from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower

# Create your models here.

class User(AbstractUser):
    pass

class Task(models.Model):
    description = models.CharField(max_length=128)
    users = models.ManyToManyField(User,related_name='tasks')

    class Meta:
        ordering = [Lower('description')]

    def __repr__(self):
        return self.description


