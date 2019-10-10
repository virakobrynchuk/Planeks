from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.

class AppUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    age = models.IntegerField(default=0)


    def as_json(self):
        context = {}
        for key, value in self.__dict__.items():
            if not (key == "_state"):
                context[key] = value
        return context

    def __str__(self):
        return self.email
