#test
from django.db import models
from ingredients.models import Ingredient

class RecipeIngredient(models.Model):
    """
    Model representing the relationship between Recipe and Ingredient.

    Fields:
    - recipe: ForeignKey linking to the Recipe model, on_delete CASCADE.
    - ingredient: ForeignKey linking to the Ingredient model, on_delete CASCADE.

    Methods:
    - __str__: Returns a string representation of the model with the format "Ingredient - Recipe".
    """
    recipe = models.ForeignKey(
        "recipes.Recipe", on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey("ingredients.Ingredient", on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the model with the format "Ingredient - Recipe".
        """
        return f"{self.ingredient} - {self.recipe}"
