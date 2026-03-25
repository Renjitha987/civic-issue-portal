from django.core.management.base import BaseCommand
from users.models import User, CitizenProfile, WardMemberProfile
from wards.models import Ward
from departments.models import Department
from complaints.models import Complaint

class Command(BaseCommand):
    help = 'Generate sample data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'Admin@123', role='ADMIN', phone_number='0000000000')

        ward1, _ = Ward.objects.get_or_create(ward_name='Ward 1 - Downtown')
        ward2, _ = Ward.objects.get_or_create(ward_name='Ward 2 - Uptown')

        head, _ = User.objects.get_or_create(username='depthead', defaults={'role': 'DEPARTMENT_HEAD', 'phone_number': '1111111111'})
        if head.role == 'DEPARTMENT_HEAD':
            head.set_password('Head@123')
            head.save()
            
        dept, _ = Department.objects.get_or_create(department_name='Waste Management', defaults={'head': head})

        wm, _ = User.objects.get_or_create(username='wardmember1', defaults={'role': 'WARD_MEMBER', 'ward': ward1, 'phone_number': '2222222222'})
        if wm.role == 'WARD_MEMBER':
            wm.set_password('Wm@12345')
            wm.save()
            WardMemberProfile.objects.get_or_create(user=wm, ward=ward1)

        citizen, _ = User.objects.get_or_create(username='citizen1', defaults={'role': 'CITIZEN', 'ward': ward1, 'phone_number': '3333333333'})
        if citizen.role == 'CITIZEN':
            citizen.set_password('Citizen@123')
            citizen.save()
            CitizenProfile.objects.get_or_create(user=citizen, aadhaar_id='123456789012', ward=ward1)

        self.stdout.write(self.style.SUCCESS('Sample data successfully created.'))
