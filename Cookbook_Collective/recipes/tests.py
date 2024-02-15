from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Recipe
from .forms import RecipeForm, SearchForm
from .views import (
    recipes_home, search_view, create_recipe, delete_account,
    recipe_difficulty_distribution, recipe_type_distribution,
    recipes_created_per_month, RecipeListView, RecipeDetailView, RecipeListViewAll
)
from .utils import (
    get_recipe_name_from_id,
    get_recipe_type_distribution_data,
    get_recipe_difficulty_distribution_data,
    render_chart
)


class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(
            name="Test Recipe",
            cooking_time=30,
            difficulty="Easy",
            min_serving_size=4,
            max_serving_size=6,
            type_of_recipe="lunch",
            ingredients="Ingredient 1, Ingredient 2",
            directions="Test directions for the recipe."
        )


    def test_recipe_name(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertEqual(recipe.name, "Test Recipe")

    def test_recipe_ingredients(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertEqual(recipe.ingredients, "Ingredient 1, Ingredient 2")

    def test_recipe_cooking_time(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertEqual(recipe.cooking_time, 30)

    def test_difficulty_calculation(self):
        recipe = Recipe.objects.get(id=1)

        self.assertEqual(recipe.calculate_difficulty(), 'Intermediate')


    def test_recipe_min_serving_size(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertEqual(recipe.min_serving_size, 4)

    def test_recipe_max_serving_size(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertEqual(recipe.max_serving_size, 6)

    def test_recipe_type_of_recipe(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertEqual(recipe.type_of_recipe, "lunch")

    def test_recipe_directions(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertEqual(recipe.directions, "Test directions for the recipe.")

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        expected_url = reverse("recipes:recipe_detail", kwargs={"pk": recipe.pk})
        self.assertEqual(recipe.get_absolute_url(), expected_url)

class RecipeViewsTest(TestCase):
    def setUp(self):
        # Create a Recipe object for testing
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            cooking_time=30,
            min_serving_size=2,
            max_serving_size=4,
            type_of_recipe='Dessert',
            ingredients='Sugar, Flour, Eggs',
            directions='Mix ingredients and bake.',
            pic='test_image.jpg',
            difficulty='Easy',
        )

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_recipes_home_view(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')

    def test_create_recipe_view_authenticated(self):
        # Create a user and log in
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Make a request to the create_recipe view
        response = self.client.get(reverse('recipes:create_recipe'))

        # Assert the expected status code
        self.assertEqual(response.status_code, 200)

    def test_create_recipe_view_not_authenticated(self):
        # Make a request to the create_recipe view without logging in
        response = self.client.get(reverse('recipes:create_recipe'))

        # Assert the expected status code (302 for redirect)
        self.assertEqual(response.status_code, 302)
        # Assert that the user is redirected to the login page
        self.assertRedirects(response, '/login/?next={}'.format(reverse('recipes:create_recipe')), status_code=302)



    def test_recipe_difficulty_distribution_view(self):
        response = self.client.get(reverse('recipes:recipe_difficulty_distribution', args=['lunch']))
        self.assertEqual(response.status_code, 302)  # Redirects if not logged in
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:recipe_difficulty_distribution', args=['lunch']))
        self.assertEqual(response.status_code, 200)

    def test_recipe_difficulty_distribution_view(self):
        response = self.client.get(reverse('recipes:recipe_difficulty_distribution', args=['lunch']))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response when logged in


    def test_recipes_created_per_month_view(self):
        response = self.client.get(reverse('recipes:recipes_created_per_month'))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response when not logged in


    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect when logged in


    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect, not 200
        self.assertRedirects(response, '/login/?next={}'.format(reverse('recipes:recipe_detail', args=[self.recipe.pk])), status_code=302)

    def test_recipe_type_distribution_template(self):
        response = self.client.get(reverse('recipes:recipe_type_distribution'))
        print(response.content.decode('utf-8'))

    def test_recipe_difficulty_distribution_template(self):
        response = self.client.get(reverse('recipes:recipe_difficulty_distribution', args=['lunch']))
        print(response.content.decode('utf-8'))  

    def test_recipes_created_per_month_template(self):
        response = self.client.get(reverse('recipes:recipes_created_per_month'))
        print(response.content.decode('utf-8'))

    def test_visualizations_template(self):
        # Make a GET request to the visualizations URL
        response = self.client.get(reverse('recipes:visualizations'))
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'recipes/visualizations.html')

    def test_visualizations_link(self):
        response = self.client.get(reverse('recipes:visualizations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recipe Difficulty Distribution")  # Check if the content is present
        
 

class RecipeFormTest(TestCase):
    def test_recipe_form_valid(self):
        form_data = {
            'name': 'Test Recipe',
            'cooking_time': 30,
            'difficulty': 'Easy',
            'min_serving_size': 4,
            'max_serving_size': 6,
            'type_of_recipe': 'lunch',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'directions': 'Test directions for the recipe.'
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_form_invalid(self):
        # Test invalid form data here
        pass

class SearchFormTest(TestCase):
    def test_search_form_invalid(self):
        # Test invalid form data for SearchForm
        invalid_form_data = {
            'query': '',  # An empty query, which is likely invalid
        }
        form = SearchForm(data=invalid_form_data)

        self.assertFalse(form.is_valid())  # Expecting the form to be invalid
        print('Errors before is_valid():', form.errors)
        self.assertTrue(form.errors)  # Check for form-level errors
        self.assertIn('query', form.errors)  # Ensure that 'query' is in the form errors





     



