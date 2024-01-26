from django.db import models
from recipes.models import Recipe



class User(models.Model): 
    username = models.CharField(max_length=120)
    saved_recipes = models.ManyToManyField(Recipe, related_name='saved_by_users', blank=True)

    def __str__(self):
        return self.username