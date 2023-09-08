from django.contrib.auth.models import AbstractUser
from django.db import models

class Author(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    full_name = models.CharField(max_length=100, verbose_name='full name')
    organization = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class VerificationToken(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    token = models.TextField(max_length=255)
    is_active = models.BooleanField(default=True)