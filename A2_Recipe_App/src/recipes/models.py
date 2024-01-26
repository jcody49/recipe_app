from django.db import models
from recipe_ingredients.models import RecipeIngredient
from ingredients.models import Ingredient
from django.shortcuts import reverse


TYPE_OF_RECIPE= (
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
)


def process_recipe_ingredients(ingredients_string):
    # Split the string into a list based on commas and spaces
    ingredients_list = [ingredient.strip() for ingredient in ingredients_string.split(',')]

    # Loop through the list and add each ingredient to the master ingredient list
    for ingredient_name in ingredients_list:
        # Check if the ingredient already exists in the database
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)

    print("Ingredients List:", ingredients_list)
    # Return the processed list of ingredients
    return ingredients_list


class Recipe(models.Model):
    name = models.CharField(max_length=120)
    cooking_time = models.PositiveIntegerField(help_text="In minutes")
    difficulty = models.CharField(max_length=50) 
    min_serving_size = models.PositiveIntegerField(help_text="Enter the minimum number of people this would serve.")
    max_serving_size = models.PositiveIntegerField(help_text="Enter the maximum number of people this would serve.") 
    type_of_recipe = models.CharField(max_length=30, choices=TYPE_OF_RECIPE)
    ingredients = models.TextField("ingredients.Ingredient", blank=True, help_text="Enter the ingredients for the recipe, separated by commas.", default="")
    directions = models.TextField(help_text="Enter the directions for preparing the recipe.")

    pic = models.ImageField(upload_to="recipes", default="no_picture.jpeg")

    def calculate_difficulty(self):
        ingredients_list = [ingredient.strip() for ingredient in self.ingredients.split(',')]
        num_ingredients = len(ingredients_list)

        if self.cooking_time < 10 and num_ingredients < 4:
            return "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            return "Intermediate"
        else:
            return "Hard"




    def save(self, *args, **kwargs):
        self.difficulty = self.calculate_difficulty()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def add_to_master_list(self):
        # Split the ingredients string by commas and strip spaces
        ingredient_list = [ingredient.strip() for ingredient in self.ingredients.split(',')]

        # Remove duplicates from the ingredient list
        unique_ingredients = list(set(ingredient_list))

        # Get the current master ingredient list (you need to define it somewhere)
        current_master_list = get_master_ingredient_list()

        # Add only the unique ingredients not already in the master list
        new_ingredients = [ingredient for ingredient in unique_ingredients if ingredient not in current_master_list]
        current_master_list.extend(new_ingredients)

        # Update the master ingredient list (you need to define the method)
        update_master_ingredient_list(current_master_list)

        # Save the changes
        self.save()


    def get_absolute_url(self):
        return reverse("recipes:recipes_detail", kwargs={"pk": self.pk})