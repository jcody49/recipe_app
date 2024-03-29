import pandas as pd
import logging
import traceback
from urllib.parse import urlparse
import sys
from urllib.parse import urlsplit
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.urls import reverse, resolve
from users.models import User
from .models import Recipe
from .forms import RecipeForm, SearchForm
from recipe_project.views import delete_account
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory

from .utils import (
    get_recipe_name_from_id,
    get_recipe_type_distribution_data,
    get_recipe_difficulty_distribution_data,
    render_chart
)
from .views import (
    recipes_home, search_view, create_recipe, 
    recipe_difficulty_distribution, recipe_type_distribution,
    recipes_created_per_month, RecipeListView, RecipeDetailView, RecipeListViewAll
)
from unittest.mock import patch, MagicMock
print("SYS PATH: ", sys.path)
logging.getLogger("matplotlib.font_manager").setLevel(logging.INFO)
#logging.getLogger('django').setLevel(logging.DEBUG)



User = get_user_model()

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

    def test_recipe_image_field(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertIsNotNone(recipe.pic)  # Ensure that the image field is not empty








class RecipeViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Testpassword1!',
        )

        # Assign specific permissions to the test user
        content_type = ContentType.objects.get_for_model(Recipe)
        add_recipe_permission = Permission.objects.get(content_type=content_type, codename='add_recipe')
        edit_recipe_permission = Permission.objects.get(content_type=content_type, codename='change_recipe')
        delete_recipe_permission = Permission.objects.get(content_type=content_type, codename='delete_recipe')
        
        self.user.user_permissions.add(add_recipe_permission, edit_recipe_permission, delete_recipe_permission)

        # Create a test recipe and assign it to self.recipe
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            cooking_time=30,
            difficulty="Easy",
            min_serving_size=4,
            max_serving_size=6,
            type_of_recipe="lunch",
            ingredients="Ingredient 1, Ingredient 2",
            directions="Test directions for the recipe."
        )

        # Record the initial user count
        self.initial_user_count = get_user_model().objects.count()
        self.client = Client()

    def tearDown(self):
        # Clean up: Delete the test user and recipe if they exist
        if self.user:
            self.user.delete()
        if self.recipe:
            self.recipe.delete()









    def test_recipe_detail_view(self):
        print("BEFORE FORCE_LOGIN - IS USER AUTHENTICATED?", self.client.session['_auth_user_id'] is not None)
        self.client.login(username='testuser', password='Testpassword1!')
        print("AFTER FORCE_LOGIN - IS USER AUTHENTICATED?", self.client.session['_auth_user_id'] is not None)
        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_recipes_home_view(self):
        
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')

    def test_create_recipe_view_authenticated(self):

        self.client.force_login(self.user)
        # Make a GET request to your create_recipe view
        response = self.client.get(reverse('recipes:create_recipe'), follow=True)  # Adjust this line

        # Check the final status code after following redirects
        self.assertEqual(response.status_code, 200)


    def test_create_recipe_view_not_authenticated(self):
        # Make a request to the create_recipe view without logging in
        response = self.client.get(reverse('recipes:create_recipe'))

        # Assert the expected status code (302 for redirect)
        self.assertEqual(response.status_code, 302)



    def test_recipe_difficulty_distribution_view(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('recipes:recipe-difficulty-distribution-detail', args=['lunch']))
        self.assertEqual(response.status_code, 200)



    def test_recipes_created_per_month_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('recipes:recipes-created-per-month-detail'))
        self.assertEqual(response.status_code, 200)


    def test_recipe_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)  # Expecting a successful access (200) when logged in




    def test_recipe_type_distribution_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('recipes:recipe-type-distribution'))

    def test_recipe_difficulty_distribution_template(self):
        self.client.force_login(self.user)

        reversed_url = reverse('recipes:recipe-difficulty-distribution-detail', args=['lunch'])



        response = self.client.get(reversed_url)


        self.assertEqual(response.status_code, 200)


    def test_recipes_created_per_month_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('recipes:recipes-created-per-month-detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_created_per_month.html')


    def test_recipe_list_all_view(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('recipes:recipe_list_all'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')  # Update with the actual template name


    def test_recipe_detail_view(self):
        is_user_authenticated = '_auth_user_id' in self.client.session and self.client.session['_auth_user_id'] is not None
        print("BEFORE FORCE_LOGIN - IS USER AUTHENTICATED?", is_user_authenticated)
        print("RECIPE DETAIL VIEW AUTHENTICATED")
        self.client.force_login(self.user)
        print("Authenticated User:", self.client.session['_auth_user_id'])
        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_search_view_with_valid_query(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')



    def test_search_view_with_empty_query(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('recipes:search'), {'query': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')



    def test_search_view_with_no_results(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('recipes:search'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')












            






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
        # Test invalid form data for RecipeForm
        invalid_form_data = {
            'name': '',
            'cooking_time': 'Invalid Value',  # Invalid input for cooking_time
            'difficulty': 'Easy',
            'min_serving_size': 4,
            'max_serving_size': 6,
            'type_of_recipe': 'lunch',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'directions': 'Test directions for the recipe.'
        }
        form = RecipeForm(data=invalid_form_data)

        self.assertFalse(form.is_valid())  # Expecting the form to be invalid
        self.assertIn('cooking_time', form.errors)  # Ensure that 'cooking_time' is in the form errors






class SearchFormTest(TestCase):
    def test_search_form_invalid(self):
        # Test invalid form data for SearchForm
        invalid_form_data = {
            'query': '',  # An empty query, which is likely invalid
        }
        form = SearchForm(data=invalid_form_data)

        self.assertFalse(form.is_valid())  # Expecting the form to be invalid
        self.assertTrue(form.errors)  # Check for form-level errors
        self.assertIn('query', form.errors)  # Ensure that 'query' is in the form errors








class RecipeUtilsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Testpassword1!',
        )
        Recipe.objects.create(
            id=1,
            name="Test Recipe",
            cooking_time=30,  # Set an appropriate value for cooking_time
            difficulty="Easy",  # Set a value for difficulty
            min_serving_size=2,  # Set a value for min_serving_size
            max_serving_size=4,  # Set a value for max_serving_size
            type_of_recipe=Recipe.BREAKFAST,  # Set a value for type_of_recipe
            ingredients="Ingredient 1, Ingredient 2",  # Set a value for ingredients
            directions="Step 1. Do this, Step 2. Do that"  # Set a value for directions
        )
        # You can set up any necessary data or configurations here
        
        pass

    def test_get_recipe_name_from_id(self):
        
        recipe_name = get_recipe_name_from_id(1)
        print("ALL RECIPES in the Database:", Recipe.objects.all())
        print("Actual Recipe Name:", recipe_name)
        self.assertEqual(recipe_name, "Test Recipe")


    def test_get_recipe_type_distribution_data(self):
        self.client.force_login(self.user)

        reversed_url = reverse('recipes:recipe-difficulty-distribution-detail', args=['lunch'])
        response = self.client.get(reversed_url)

        self.assertEqual(response.status_code, 200)



   



    def test_render_chart(self):
        # Test when data is available
        data = pd.DataFrame({'recipe_type': ['type1', 'type2'], 'count': [10, 20]})
        chart_image = render_chart(request=None, chart_type=1, data=data)

        expected_prefix = 'iVBORw0KGgoAAAANSUhEUgAABLAAAAMgCAYAAAAz4JsCAAAAOX'


        self.assertTrue(chart_image.startswith(expected_prefix), "Chart image does not start with the expected prefix.")







class AuthViewsTest(TestCase):

    def test_login_view_with_valid_credentials(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'), follow=True)

        # Expect 200 if the user is authenticated and redirected to the home page
        self.assertEqual(response.status_code, 200, msg=f"Unexpected status code: {response.status_code}")

    def test_login_view_with_invalid_credentials(self):
        # Test login view with invalid credentials
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})

        # Check for a 401 Unauthorized status code
        self.assertEqual(response.status_code, 401, msg=f"Unexpected status code: {response.status_code}")







    def test_logout_view(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='Testpassword1!', email='testuser@email.com')
        self.client.login(username='testuser', password='Testpassword1!')

        response = self.client.get(reverse('logout'))

        # Assert the redirect and other response details
        #self.assertRedirects(response, reverse('success'))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)




    def test_signup_view_with_valid_data(self):
        # Test signup view with valid data
        response = self.client.post(reverse('signup'), {'username': 'testuser', 'password1': 'Testpassword1!', 'password2': 'Testpassword1!'})

        # Check if the response is a redirect
        if response.status_code == 302:
            # If it's a redirect, assert the redirection
            self.assertIn(reverse('home'), response.url)
        else:
            # If it's not a redirect, assert the content and status code
            self.assertEqual(response.status_code, 200)





    def test_signup_view_with_invalid_data(self):
        # Test signup view with invalid data
        response = self.client.post(reverse('signup'), {'username': '', 'password1': 'password', 'password2': 'password'})

        # Check for a redirect response (status code 200)
        self.assertEqual(response.status_code, 200, msg=f"Unexpected status code: {response.status_code}")


