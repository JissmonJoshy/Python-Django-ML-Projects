import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from myapp.models import User

# Delete existing admin if exists
User.objects.filter(username='admin').delete()

# Create superuser using custom User model
try:
    superuser = User.objects.create(
        username='admin',
        email='admin@gmail.com',
        name='Admin User',
        number='9999999999',
        password=make_password('admin@123'),
        is_staff=True,
        is_superuser=True
    )
    print("✓ Superuser created successfully!")
    print(f"  Username: admin")
    print(f"  Email: admin@gmail.com")
    print(f"  Password: admin@123")
    print(f"  User ID: {superuser.id}")
except Exception as e:
    print(f"Error: {e}")
