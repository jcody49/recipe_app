from django.db import models
from django.shortcuts import reverse
from ingredients.models import Ingredient

TYPE_OF_RECIPE = (
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
)

DIFFICULTY_LEVELS = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Intermediate', 'Intermediate'),
    ('Hard', 'Hard'),
)


def process_recipe_ingredients(ingredients_string):
    """
    Process a string of ingredients, split it into a list, and add each ingredient to the database.

    Args:
        ingredients_string (str): String containing ingredients separated by commas.

    Returns:
        list: List of processed ingredients.
    """
    ingredients_list = [ingredient.strip() for ingredient in ingredients_string.split(',')]

    for ingredient_name in ingredients_list:
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)

    return ingredients_list


class Recipe(models.Model):
    """
    Model representing a recipe.
    """
    name = models.CharField(max_length=120)
    cooking_time = models.PositiveIntegerField(help_text="In minutes")
    difficulty = models.CharField(max_length=50)
    min_serving_size = models.PositiveIntegerField(help_text="Enter the minimum number of people this would serve.")
    max_serving_size = models.PositiveIntegerField(help_text="Enter the maximum number of people this would serve.")
    type_of_recipe = models.CharField(max_length=30, choices=TYPE_OF_RECIPE)
    ingredients = models.TextField("ingredients.Ingredient", blank=True,
                                   help_text="Enter the ingredients for the recipe, separated by commas.", default="")
    directions = models.TextField(help_text="Enter the directions for preparing the recipe.")
    pic = models.ImageField(upload_to='recipes/', null=True, blank=True, default='recipes/no_picture.jpeg')

    def calculate_difficulty(self):
        """
        Calculate the difficulty level of the recipe based on cooking time and number of ingredients.

        Returns:
            str: Calculated difficulty level.
        """
        ingredients_list = [ingredient.strip() for ingredient in self.ingredients.split(',')]
        num_ingredients = len(ingredients_list)

        if self.cooking_time < 10 and num_ingredients < 4:
            calculated_difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            calculated_difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            calculated_difficulty = "Intermediate"
        else:
            calculated_difficulty = "Hard"

        return calculated_difficulty

    def save(self, *args, **kwargs):
        """
        Override the save method to calculate and set the difficulty before saving.
        """
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the Recipe.
        """
        return self.name

    def add_to_master_list(self):
        """
        Add unique ingredients from the recipe to the master ingredient list.
        """
        ingredient_list = [ingredient.strip() for ingredient in self.ingredients.split(',')]
        unique_ingredients = list(set(ingredient_list))
        current_master_list = get_master_ingredient_list()
        new_ingredients = [ingredient for ingredient in unique_ingredients if ingredient not in current_master_list]
        current_master_list.extend(new_ingredients)
        update_master_ingredient_list(current_master_list)
        self.save()

    def get_absolute_url(self):
        """
        Get the absolute URL for the recipe detail page.

        Returns:
            str: Absolute URL for the recipe detail page.
        """
        return reverse("recipes:recipe_detail", kwargs={"pk": self.pk})
