from django.core.management.base import BaseCommand
from core_auth.models import Role, BusinessElement, AccessRule, User

class Command(BaseCommand):
    help = 'Populates the database with demo roles, elements, and access rules.'

    def handle(self, *args, **options):
        self.stdout.write("Creating demo data...")

        # Создание ролей
        dev_role, _ = Role.objects.get_or_create(name='Developer', description='Has read and update access to code.')
        qa_role, _ = Role.objects.get_or_create(name='QA', description='Has read access to tests and results.')

        # Создание бизнес-элементов
        code_be, _ = BusinessElement.objects.get_or_create(name='code', description='Source code files.')
        tests_be, _ = BusinessElement.objects.get_or_create(name='tests', description='Test cases and results.')

        # Создание правил доступа
        AccessRule.objects.get_or_create(role=dev_role, business_element=code_be, read_permission=True, update_permission=True)
        AccessRule.objects.get_or_create(role=qa_role, business_element=tests_be, read_permission=True)

        self.stdout.write(self.style.SUCCESS('Successfully populated database with demo data.'))