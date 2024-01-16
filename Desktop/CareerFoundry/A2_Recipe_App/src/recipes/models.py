from django.db import models


TYPE_OF_RECIPE= (
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
)

class Recipe(models.Model):
    name = models.CharField(max_length=120)
    ingredients = models.CharField(max_length=255)
    cooking_time = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=50) 
    min_serving_size = models.PositiveIntegerField()
    max_serving_size = models.PositiveIntegerField() 
    type_of_recipe = models.CharField(max_length=30, choices=TYPE_OF_RECIPE)
    directions = models.TextField()

    def __str__(self):
        return self.name

