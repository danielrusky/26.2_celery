from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        group_name = 'Модераторы'
        moderator_name = 'moderator1'
        moderator_email = f'{moderator_name}@sky.pro'
        moderator_password = 'password123'

        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            group = Group.objects.create(name=group_name)
            print(f'Создана группа модераторов: {group_name}')

        user, created = User.objects.get_or_create(
            email=moderator_email,
            defaults={
                'first_name': moderator_name,
                'is_superuser': False,
                'is_staff': True,
                'is_active': True,
                'role': 'moderator'
            }
        )

        if created or not user.groups.filter(name=group_name).exists():
            user.set_password(moderator_password)
            user.save()
            user.groups.add(group)
            print(f'Пользователь {user.email} добавлен в группу модераторов')
        else:
            print(f'Пользователь {user.email} уже является модератором')