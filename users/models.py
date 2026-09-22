from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (('student', 'Student'), ('staff', 'Staff'), ('admin', 'Admin'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_suspended = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} ({self.role})'
