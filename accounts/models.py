from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.
class CustomUser(AbstractUser):
    ROLES = [
        ('player', 'Player'),
        ('gameKeeper', 'Game Keeper'),
        ('developer', 'Developer'),
    ]

    role = models.CharField(max_length=50, choices=ROLES, default='player')
    verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    creationDateTime = models.DateTimeField(auto_now_add=True)