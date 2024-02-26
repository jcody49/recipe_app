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
        # Assert that the user is redirected to the login page
        self.assertRedirects(response, '/login/?next={}'.format(reverse('recipes:create_recipe')), status_code=302)


    def test_recipe_difficulty_distribution_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('recipes:recipe_difficulty_distribution', args=['lunch']))
        self.assertEqual(response.status_code, 302)  # Redirects if not logged in
        response = self.client.get(reverse('recipes:recipe_difficulty_distribution', args=['lunch']))
        self.assertEqual(response.status_code, 200)


    def test_recipes_created_per_month_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('recipes-created-per-month-detail'))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response when not logged in


    def test_recipe_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)  # Expecting a successful access (200) when logged in




    def test_recipe_type_distribution_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('recipes:recipe_type_distribution'))


    def test_recipe_difficulty_distribution_template(self):
        self.client.force_login(self.user)
        print("RDD TEMPLATE")
        reversed_url = reverse('recipe-difficulty-distribution-detail', args=['lunch'])
        print("Reversed URL:", reversed_url)

        response = self.client.get(reversed_url)
        print("Response Content:", response.content)
        print("Response Headers:", response.headers)

        self.assertEqual(response.status_code, 200)


    def test_recipes_created_per_month_template(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('recipes-created-per-month-detail'))



    def test_delete_account_redirect_to_login(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('recipes:delete_account'))

        # Check if the user is redirected upon successful deletion
        self.assertRedirects(response, reverse('login'))

        # Optionally, check if the user is no longer authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)






    def test_delete_account_view_not_authenticated(self):

        response = self.client.get(reverse('recipes:delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next={}'.format(reverse('recipes:delete_account')), status_code=302)

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
        response = self.client.get(reverse('recipes:search_view'), {'query': 'Sugar'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')
        self.assertContains(response, 'Search Results for "Sugar"')

    def test_search_view_with_empty_query(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('recipes:search_view'), {'query': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')
        self.assertContains(response, 'Please enter a valid search query')

    def test_search_view_with_no_results(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('recipes:search_view'), {'query': 'Nonexistent Ingredient'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')
        self.assertContains(response, 'No recipes found for your search query')











            






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
        # You can set up any necessary data or configurations here
        pass

    def test_get_recipe_name_from_id(self):
        recipe_name = get_recipe_name_from_id(1)
        self.assertEqual(recipe_name, "Test Recipe")

    def test_get_recipe_type_distribution_data(self):
        # Test when there is data available
        data = get_recipe_type_distribution_data(type_of_recipe='lunch')
        self.assertFalse(data.empty)
        self.assertIn('recipe_type', data.columns)
        self.assertIn('count', data.columns)

        # Test when there is no data available
        data = get_recipe_type_distribution_data(type_of_recipe='invalid_type')
        self.assertTrue(data.empty)

    def test_get_recipe_difficulty_distribution_data(self):
        # Test when there is data available
        data = get_recipe_difficulty_distribution_data(request=None, type_of_recipe='lunch')
        self.assertIsInstance(data, pd.DataFrame)  # Ensure it's a DataFrame
        self.assertFalse(data.empty)
        self.assertIn('difficulty', data.columns)
        self.assertIn('count', data.columns)

        # Test when there is no data available
        data = get_recipe_difficulty_distribution_data(request=None, type_of_recipe='invalid_type')
        self.assertIsInstance(data, HttpResponse)  # Ensure it's an HttpResponse
        self.assertEqual(data.status_code, 204)  # Assuming 204 is used for no data response


    def test_render_chart(self):
        # Test when data is available
        data = pd.DataFrame({'recipe_type': ['type1', 'type2'], 'count': [10, 20]})
        chart_image = render_chart(request=None, chart_type=1, data=data)
        self.assertTrue(chart_image.startswith('data:image/png;base64,'))

        # Test when data is not available
        chart_image = render_chart(request=None, chart_type=1, data=None)
        self.assertEqual(chart_image, "No data available for rendering the chart.")






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
        User = get_user_model()
        User.objects.create_user(username='testuser', password='testpassword')

        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})

        # Check for a failed login and the correct redirect
        self.assertEqual(response.status_code, 301, msg="Login failed and redirected as expected")

    def test_logout_view(self):
        # Test logout view
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('logout'))

        # Assert the redirect and other response details
        self.assertRedirects(response, reverse('success_page'), status_code=302)
        self.assertContains(response, 'successfully logged out', html=True)
        self.assertEqual(response.status_code, 200, msg=f"Unexpected status code: {response.status_code}")

    def test_signup_view_with_valid_data(self):
        response = self.client.post(reverse('signup'), {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})

        # Assert the expected URL for the home page
        expected_home_url = reverse('home')
        self.assertIn(expected_home_url, response.url)

    def test_signup_view_with_invalid_data(self):
        # Test signup view with invalid data
        response = self.client.post(reverse('signup'), {'username': '', 'password1': 'password', 'password2': 'password'})

        # Check for a redirect response (status code 300-399)
        self.assertTrue(300 <= response.status_code < 400, msg=f"Unexpected status code: {response.status_code}")

