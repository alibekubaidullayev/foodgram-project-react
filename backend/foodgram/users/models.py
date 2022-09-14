from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

MAX_LENGTH = 200
USER = "user"
ADMIN = "admin"
USERNAME_LENGTH = 150
EMAIL_LENGTH = 254
NAME_ARGS = {"max_length": USERNAME_LENGTH, "blank": True, "null": True}
ROLES = {(USER, "User"), (ADMIN, "Administrator")}


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        return self.create_user(email, password, **kwargs)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=EMAIL_LENGTH, unique=True, verbose_name="Электронная почта"
    )
    username = models.CharField(
        "Имя пользователя",
        max_length=USERNAME_LENGTH,
        unique=True,
    )
    first_name = models.CharField(verbose_name="Имя", **NAME_ARGS)
    last_name = models.CharField(verbose_name="Фамилия", **NAME_ARGS)
    role = models.CharField(
        verbose_name="Роль",
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_full_name(self):
        return f"{self.first_name}{self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
