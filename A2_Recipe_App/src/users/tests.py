from django.test import TestCase

from .models import User
from recipes.models import Recipe

class UserModelTest(TestCase):
    def setUp(self):
        recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="Ingredient 1, Ingredient 2",
            cooking_time=30,
            difficulty="Intermediate",
            min_serving_size=4,
            max_serving_size=6,
            type_of_recipe="lunch",
            directions="Test directions for the recipe."
        )

        user = User.objects.create(username="testuser")
        user.saved_recipes.set([recipe])  # Use set() with a list of recipes

    def test_user_username(self):
        user = User.objects.get(username="testuser")
        self.assertEqual(user.username, "testuser")
