import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from myapp.models import User

# Create admin user
admin = User(
    name='Admin User',
    email='admin@example.com',
    number='9999999999',
    password=make_password('Admin@123'),
    is_staff=True
)
admin.save()

print("✓ Admin user created successfully!")
print(f"  Email: admin@example.com")
print(f"  Password: Admin@123")
print(f"  User ID: {admin.id}")
