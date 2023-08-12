from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_demo_account = models.BooleanField(default=False)
