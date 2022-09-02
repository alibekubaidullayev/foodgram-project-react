from django.db import models

from django.contrib.auth.models import AbstractUser

MAX_LENGTH = 200
USER = 'user'
ADMIN = 'admin'
USERNAME_LENGTH = 150
EMAIL_LENGTH = 254
CONFIRMATION_CODE_LENGTH = 6

ROLES = {
    (USER, 'User'),
    (ADMIN, 'Administrator')
}

class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True
    )

    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    class Meta:
        ordering = ["username", ]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
