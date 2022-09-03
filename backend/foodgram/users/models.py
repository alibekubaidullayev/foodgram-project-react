from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

MAX_LENGTH = 200
USER = 'user'
ADMIN = 'admin'
USERNAME_LENGTH = 150
EMAIL_LENGTH = 254

ROLES = {
    (USER, 'User'),
    (ADMIN, 'Administrator')
}


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **kwargs)
        
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email,  password=None, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        unique=True,
        verbose_name='Электронная почта'
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_LENGTH,
        unique=True,
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_LENGTH,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=USERNAME_LENGTH,
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER
    )

    objects = UserManager()

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return f"{self.first_name}{self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
