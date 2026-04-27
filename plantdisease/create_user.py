import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from myapp.models import User

# Delete existing test user if exists
User.objects.filter(email='user@example.com').delete()

# Create regular user
try:
    user = User.objects.create(
        username='testuser',
        email='user@example.com',
        name='Test User',
        number='9876543210',
        password=make_password('user@123'),
        is_staff=False
    )
    print("✓ Regular user created successfully!")
    print(f"  Email: user@example.com")
    print(f"  Password: user@123")
    print(f"  User ID: {user.id}")
except Exception as e:
    print(f"Error: {e}")
