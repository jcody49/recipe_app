from django.db import models

# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return str(self.name)