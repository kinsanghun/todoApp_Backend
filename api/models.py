from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from django.utils.translation import gettext_lazy as _


class Users(AbstractUser):
    username = None
    email = models.CharField(max_length=30, unique=True)
    userPassword = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Todos(models.Model):
    user = models.ForeignKey("Users", related_name="users", on_delete=models.CASCADE, db_column="userId")
    title = models.CharField(max_length=100)
    description = models.TextField()
    isChecked = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()