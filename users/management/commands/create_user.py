from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_name = 'user5'
        user_email = f'{user_name}@sky.pro'
        user_password = '123password'

        if User.objects.filter(email=user_email).exists():
            print(f'Пользователь с email {user_email} уже существует')
            return

        user, created = User.objects.get_or_create(
            email=user_email,
            defaults={
                'first_name': user_name,
                'is_superuser': False,
                'is_staff': False,
                'is_active': True,
                'role': 'member'
            }
        )
        user.set_password(user_password)
        user.save()