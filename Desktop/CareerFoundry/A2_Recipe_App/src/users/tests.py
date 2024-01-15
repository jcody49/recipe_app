from django.test import TestCase
from .models import User
from recipes.models import Recipe

class UserModelTest(TestCase):
    def setUp(self):
        recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="Ingredient 1, Ingredient 2",
            cooking_time=30,
            difficulty="Easy",
            min_serving_size=4,
            max_serving_size=6,
            type_of_recipe="lunch",
            directions="Test directions for the recipe."
        )

        User.objects.create(
            username="testuser",
            saved_recipes=recipe
        )

    def test_user_username(self):
        user = User.objects.get(username="testuser")
        self.assertEqual(user.username, "testuser")
