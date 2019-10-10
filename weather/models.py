from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=30)
    temp = models.IntegerField(default=0)
    img = models.CharField(max_length=256)

    def __str__(self):
        return self.name
