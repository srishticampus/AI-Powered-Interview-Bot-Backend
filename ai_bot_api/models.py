from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, blank=False, default="Default Name")
    phone_number = models.CharField(max_length=15, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']  