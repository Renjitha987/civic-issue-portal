from django.db import models
from django.conf import settings

class Department(models.Model):
    department_name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    head = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'role': 'DEPARTMENT_HEAD'},
        related_name='headed_departments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department_name
