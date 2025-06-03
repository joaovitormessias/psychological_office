from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.TextChoices):
    SECRETARIA = 'SECRETARIA', 'Secretaria'
    PROFISSIONAL_SAUDE = 'PROFISSIONAL_SAUDE', 'Profissional de Saúde'
    ADMIN = 'ADMIN', 'Administrador' # Adding Admin for superuser flexibility

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.ADMIN, # Default to Admin, can be changed as needed
    )
    # Add any other common fields if necessary, e.g., created_at, updated_at
    # For now, keeping it simple as per requirements focusing on role.

    def __str__(self):
        return self.username
