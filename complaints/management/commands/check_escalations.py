from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from complaints.models import Complaint
from users.models import User
from audit.models import AuditLog
from notifications.models import Notification

class Command(BaseCommand):
    help = 'Check and escalate complaints older than 30 days.'

    def handle(self, *args, **kwargs):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        twenty_five_days_ago = timezone.now() - timedelta(days=25)
        
        warnings = Complaint.objects.filter(
            status__in=['Pending', 'In Progress', 'Forwarded'], 
            date_submitted__lte=twenty_five_days_ago, 
            date_submitted__gt=thirty_days_ago,
            priority_level='Normal'
        )
        for w in warnings:
            w.priority_level = 'Warning'
            w.save(update_fields=['priority_level'])

        escalations = Complaint.objects.filter(
            status__in=['Pending', 'In Progress', 'Forwarded'], 
            date_submitted__lte=thirty_days_ago,
            is_escalated=False
        )
        
        admin_users = User.objects.filter(role='ADMIN')
        
        count = 0
        for comp in escalations:
            comp.status = 'Escalated'
            comp.priority_level = 'Critical'
            comp.is_escalated = True
            comp.escalation_date = timezone.now()
            comp.save()
            count += 1
            
            AuditLog.objects.create(
                user=None,
                action='System Auto-Escalation',
                description=f'Complaint {comp.id} escalated automatically due to 30 days timeout.'
            )
            
            for admin in admin_users:
                Notification.objects.create(
                    sender=comp.citizen,
                    receiver=admin,
                    message=f'System Alert: Complaint {comp.id} has been automatically escalated.'
                )
                
            if comp.department and comp.department.head:
                Notification.objects.create(
                    sender=comp.citizen,
                    receiver=comp.department.head,
                    message=f'System Alert: Complaint {comp.id} in your department has been escalated.'
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully escalated {count} complaints.'))
