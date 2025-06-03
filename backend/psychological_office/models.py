from django.db import models
from django.contrib.auth.models import AbstractUser

#------------------------ CREATING MODELS ------------------------#

class Patient (models.Model):
    cpf = models.CharField(unique=True, max_length=11)
    patient_name = models.CharField(max_length=100)
    dob = models.DateField()
    address = models.JSONField()
    contact = models.JSONField()

    def __str__(self):
        return self.patient_name

class User(AbstractUser):
    ROLE_CHOICES = [('SECRETARIA', 'Secretaria'), ('PROFISSIONAL_SAUDE', 'Profissional de Saúde')]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank = True
    )

    def __str__(self):
        return self.role
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('Schuduled','Schuduled'), ('Cancelled','Cancelled')])

    def __str__(self):
        return self.patient.patient_name

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('In Progress', 'In Progress'), ('Completed', 'Completed')])
    notes = models.TextField()

    def __str__(self):
        return self.patient