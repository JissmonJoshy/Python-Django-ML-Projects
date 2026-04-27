from django.core.management.base import BaseCommand
from myapp.models import User

class Command(BaseCommand):
    help = 'Create an admin user'

    def handle(self, *args, **options):
        # Check if admin already exists
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists'))
            return

        # Create admin user
        admin = User.objects.create_user(
            username='admin',
            email='admin@marketplace.com',
            name='Admin User',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        
        self.stdout.write(self.style.SUCCESS('Admin user created successfully!'))
        self.stdout.write(f'Username: admin')
        self.stdout.write(f'Password: admin123')
