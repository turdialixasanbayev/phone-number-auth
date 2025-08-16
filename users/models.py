from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    STATUS = (
        ('active', 'Active'),
        ('deactive', 'Deactive')
    )
    username = None
    first_name = None
    last_name = None
    email = None
    phone_number = models.CharField(max_length=15, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default='active')

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.pk} - {self.phone_number}"
