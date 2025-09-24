from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core_auth.models import User

class AuthAPITests(APITestCase):
    
    def setUp(self):
        """
        Настройка для тестов: создаем тестовые данные и клиента API.
        """
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

    def _get_auth_token(self):
        """
        Вспомогательный метод для регистрации/логина и получения токена.
        """
        self.client.post(self.registration_url, self.user_data, format='json')
        response = self.client.post(self.login_url, self.login_data, format='json')
        return response.data['access']

    def test_registration(self):
        """
        Тест успешной регистрации нового пользователя.
        """
        response = self.client.post(self.registration_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_login(self):
        """
        Тест успешного входа в систему после регистрации.
        """
        self.client.post(self.registration_url, self.user_data, format='json')
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_profile(self):
        """
        Тест получения данных профиля для аутентифицированного пользователя.
        """
        access_token = self._get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get(self.profile_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_update_profile(self):
        """
        Тест частичного обновления профиля пользователя.
        """
        access_token = self._get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        update_data = {'first_name': 'NewName'}
        response = self.client.patch(self.profile_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'NewName')

    def test_soft_delete(self):
        """
        Тест "мягкого" удаления аккаунта.
        """
        access_token = self._get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        user = User.objects.get(email='testuser@example.com')
        self.assertFalse(user.is_active)