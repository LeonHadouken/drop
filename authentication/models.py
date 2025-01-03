# models.py
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
