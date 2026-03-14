from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    Role_choices = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('author', 'Author'),
        ('reader', 'Reader'),
    )

  
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.username
