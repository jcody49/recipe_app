from django.db import models
from ingredients.models import Ingredient

# Create your models here.

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        "recipes.Recipe", on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey("ingredients.Ingredient", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ingredient} - {self.recipe}"