
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.

# CustomUser inherits the functions and attributes of AbstactUser
class CustomUser(AbstractUser):
    # Ensures the role of player can only be one of three
    ROLES = [
        ('player', 'Player'),
        ('gameKeeper', 'Game Keeper'),
        ('developer', 'Developer'),
    ]

    # Additional custom attributes not inherited from AbstractUser
    role = models.CharField(max_length=50, choices=ROLES, default='player')
    verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    creationDateTime = models.DateTimeField(auto_now_add=True)



