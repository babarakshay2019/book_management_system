# models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Set is_staff for superuser
        extra_fields.setdefault('is_superuser', True)  # Set is_superuser for superuser

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('admin', _('Admin')),
        ('user', _('User')),
    ]

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='user',  # Default to 'user'
    )
    is_active = models.BooleanField(default=True)  # Indicates if the user is active
    is_staff = models.BooleanField(default=False)  # Indicates if the user can log into the admin site
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']  # Specify required fields

    def __str__(self):
        return self.email
