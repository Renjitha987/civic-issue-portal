from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Complaint, ComplaintForwarding, Remark
from notifications.models import Notification
from audit.models import AuditLog

@receiver(post_save, sender=Complaint)
def log_complaint_creation(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(
            user=instance.citizen,
            action='Created Complaint',
            description=f'Complaint {instance.id} created under category {instance.issue_category}'
        )
        if instance.assigned_to:
            Notification.objects.create(
                sender=instance.citizen,
                receiver=instance.assigned_to,
                message=f'New complaint {instance.id} assigned to you.'
            )

@receiver(post_save, sender=ComplaintForwarding)
def notify_on_forward(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(
            user=instance.forwarded_by,
            action='Forwarded Complaint',
            description=f'Complaint {instance.complaint.id} forwarded to {instance.department.department_name}'
        )
        if instance.department.head:
            Notification.objects.create(
                sender=instance.forwarded_by,
                receiver=instance.department.head,
                message=f'Complaint {instance.complaint.id} was forwarded to your department.'
            )

@receiver(post_save, sender=Remark)
def notify_on_remark(sender, instance, created, **kwargs):
    if created:
        if instance.added_by != instance.complaint.citizen:
            Notification.objects.create(
                sender=instance.added_by,
                receiver=instance.complaint.citizen,
                message=f'A new remark was added to your complaint {instance.complaint.id}.'
            )
