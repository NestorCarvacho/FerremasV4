from django.core.management.base import BaseCommand
from entrega.models import User

class Command(BaseCommand):
    help = 'Create a superuser if one does not exist'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
        else:
            User.objects.create_superuser(
                username='admin',
                email='admin@admin.com',
                password='admin123',
                user_type='employee'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
