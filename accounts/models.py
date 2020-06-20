from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user
class CustomUser(AbstractUser):
    """　拡張ユーザモデル """

    class Meta:
        verbose_name_plural = "CustomUser"
