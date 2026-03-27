import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civic_portal.settings')
django.setup()

from users.models import User
from departments.models import Department

dept, created = Department.objects.get_or_create(department_name='Health')

if not dept.head:
    # Create or get health head
    head_user, user_created = User.objects.get_or_create(
        username='health_head', 
        defaults={'role': 'DEPARTMENT_HEAD', 'full_name': 'Health Department Head', 'phone_number': '4444444444'}
    )
    dept.head = head_user
    dept.save()
else:
    head_user = dept.head

head_user.set_password("Health@123")
head_user.save()

print(f"Username: {head_user.username}\nPassword: Health@123")
