from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core_auth.models import User, Role, BusinessElement, AccessRule

class AuthAPITests(APITestCase):
    
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'strongpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.login_data = {
            'email': 'testuser@example.com',
            'password': 'strongpassword123'
        }
        self.registration_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.delete_url = reverse('delete')
        self.test_resource_url = reverse('test-resource')
        self.superuser = User.objects.create_superuser('admin@test.com', 'admin_password')

    def _get_auth_token(self, user_data=None):
        if user_data is None:
            user_data = self.user_data
        
        self.client.post(self.registration_url, user_data, format='json')
        response = self.client.post(self.login_url, user_data, format='json')
        return response.data['access']

    def _get_superuser_token(self):
        response = self.client.post(self.login_url, {'email': 'admin@test.com', 'password': 'admin_password'}, format='json')
        if response.status_code != status.HTTP_200_OK:
            raise Exception(f"Superuser login failed with status {response.status_code}")
        return response.data['access']

    def test_registration(self):
        initial_user_count = User.objects.count()
        response = self.client.post(self.registration_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), initial_user_count + 1)
        self.assertEqual(User.objects.get(email='testuser@example.com').email, 'testuser@example.com')

    def test_login(self):
        self.client.post(self.registration_url, self.user_data, format='json')
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_profile(self):
        access_token = self._get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.profile_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_update_profile(self):
        access_token = self._get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        update_data = {'first_name': 'NewName'}
        response = self.client.patch(self.profile_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'NewName')

    def test_soft_delete(self):
        access_token = self._get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user = User.objects.get(email='testuser@example.com')
        self.assertFalse(user.is_active)

    def test_access_to_test_resource(self):
        user_with_access = User.objects.create_user(email='access@example.com', password='password123')
        access_role = Role.objects.create(name='access_role')
        user_with_access.role = access_role
        user_with_access.save()
        BusinessElement.objects.create(name='test_resource')
        AccessRule.objects.create(role=access_role, business_element=BusinessElement.objects.get(name='test_resource'), read_permission=True)
        
        access_token = self._get_auth_token(user_data={'email': 'access@example.com', 'password': 'password123'})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.test_resource_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        user_no_access = User.objects.create_user(email='noaccess@example.com', password='password123')
        no_access_role = Role.objects.create(name='no_access_role')
        user_no_access.role = no_access_role
        user_no_access.save()
        AccessRule.objects.create(role=no_access_role, business_element=BusinessElement.objects.get(name='test_resource'), read_permission=False)
        
        no_access_token = self._get_auth_token(user_data={'email': 'noaccess@example.com', 'password': 'password123'})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {no_access_token}')
        response = self.client.get(self.test_resource_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_role(self):
        initial_role_count = Role.objects.count()
        token = self._get_superuser_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        role_data = {'name': 'test_admin_role', 'description': 'Role created via API'}
        response = self.client.post(reverse('role-list'), role_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), initial_role_count + 1)
        self.assertEqual(Role.objects.get(name='test_admin_role').description, 'Role created via API')

    def test_admin_create_business_element(self):
        initial_be_count = BusinessElement.objects.count()
        token = self._get_superuser_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        be_data = {'name': 'test_admin_be', 'description': 'Business element created via API'}
        response = self.client.post(reverse('business-element-list'), be_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BusinessElement.objects.count(), initial_be_count + 1)
        self.assertEqual(BusinessElement.objects.get(name='test_admin_be').description, 'Business element created via API')

    def test_admin_create_access_rule(self):
        initial_rule_count = AccessRule.objects.count()
        token = self._get_superuser_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        test_role = Role.objects.create(name='test_rule_role')
        test_be = BusinessElement.objects.create(name='test_rule_be')
        rule_data = {
            'role': test_role.id,
            'business_element': test_be.id,
            'read_permission': True
        }
        response = self.client.post(reverse('access-rule-list'), rule_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AccessRule.objects.count(), initial_rule_count + 1)
        self.assertTrue(AccessRule.objects.get(role=test_role, business_element=test_be).read_permission)