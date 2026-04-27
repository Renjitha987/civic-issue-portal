from django.db import models

class Panchayat(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Ward(models.Model):
    ward_name = models.CharField(max_length=100, unique=True)
    panchayat = models.ForeignKey(Panchayat, on_delete=models.SET_NULL, null=True, blank=True, related_name='wards')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ward_name

