from django.apps import AppConfig
from django.core.exceptions import ObjectDoesNotExist

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        self.create_author_group()

    def create_author_group(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Post  # Импортируйте свою модель здесь

        try:
            # Создаем группу "Автор"
            group, group_created = Group.objects.get_or_create(name='Автор')

            # Создаем разрешение
            content_type = ContentType.objects.get_for_model(Post)
            permission, permission_created = Permission.objects.get_or_create(
                codename='can_edit_post',
                name='Can edit posts',
                content_type=content_type
            )
            if permission_created:
                print(f'Permission "{permission.name}" created.')
            else:
                print(f'Permission "{permission.name}" already exists.')

            # Назначаем разрешение группе
            if permission_created:
                group.permissions.add(permission)
                print(f'Permission "{permission.name}" added to group "{group.name}".')

        except ObjectDoesNotExist as e:
            print(f'Error occurred: {e}')

