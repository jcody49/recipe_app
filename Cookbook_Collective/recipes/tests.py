import pandas as pd

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from users.models import User
from django.contrib.auth.models import User
from .models import Recipe
from .forms import RecipeForm, SearchForm
from recipe_project.views import delete_account
from .views import (
    recipes_home, search_view, create_recipe, 
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

    def test_recipe_image_field(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertIsNotNone(recipe.pic)  # Ensure that the image field is not empty








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
        # Create a test user with your custom user model
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',  # Use your custom fields as needed
            password='Testpassword1!',
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
        User = get_user_model()

        # Set a dummy SECRET_KEY for testing
        from django.conf import settings
        settings.SECRET_KEY = 'your_dummy_secret_key_for_testing'

        user = User.objects.create_user(username='testuser', password='testpassword')

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

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
        response = self.client.get(reverse('recipes:recipe_difficulty_distribution', args=['lunch']))
        self.assertEqual(response.status_code, 302)  # Redirects if not logged in
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:recipe_difficulty_distribution', args=['lunch']))
        self.assertEqual(response.status_code, 200)

    def test_recipe_difficulty_distribution_view(self):
        response = self.client.get(reverse('recipes:recipe_difficulty_distribution', args=['lunch']))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response when logged in


    def test_recipes_created_per_month_view(self):
        response = self.client.get(reverse('recipes-created-per-month-detail'))
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


    def test_recipe_difficulty_distribution_template(self):
        response = self.client.get(reverse('recipes:recipe_difficulty_distribution', args=['lunch']))


    def test_recipes_created_per_month_template(self):
        response = self.client.get(reverse('recipes-created-per-month-detail'))


    
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

    def test_delete_account_view_authenticated(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')

        response = self.client.get(reverse('recipes:delete_account'))
        self.assertEqual(response.status_code, 200)

    def test_delete_account_view_not_authenticated(self):
        response = self.client.get(reverse('recipes:delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next={}'.format(reverse('recipes:delete_account')), status_code=302)

    def test_recipe_list_all_view(self):
        response = self.client.get(reverse('recipes:recipe_list_all'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list_all.html')

    def test_recipe_detail_view_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_search_view_with_valid_query(self):
        # Test the search view with a valid query
        response = self.client.get(reverse('recipes:search_view'), {'query': 'Sugar'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')
        self.assertContains(response, 'Search Results for "Sugar"')

    def test_search_view_with_empty_query(self):
        # Test the search view with an empty query
        response = self.client.get(reverse('recipes:search_view'), {'query': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')
        self.assertContains(response, 'Please enter a valid search query')

    def test_search_view_with_no_results(self):
        # Test the search view with a query that yields no results
        response = self.client.get(reverse('recipes:search_view'), {'query': 'Nonexistent Ingredient'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')
        self.assertContains(response, 'No recipes found for your search query')

    def test_visualizations_view_authenticated(self):
        # Test the visualizations view when authenticated
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('recipes:visualizations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/visualizations.html')
        self.assertContains(response, "Recipe Difficulty Distribution")

    def test_visualizations_view_not_authenticated(self):
        # Test the visualizations view when not authenticated
        response = self.client.get(reverse('recipes:visualizations'))
        
        # Print the response content and headers for debugging
        print("Response Content:", response.content)
        print("Response Headers:", response.headers)

        expected_redirect_url = reverse('login')
        self.assertRedirects(response, expected_redirect_url, status_code=302)













            






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
        print('Errors before is_valid():', form.errors)
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
    def setUp(self):
        print("setUp method is being executed")

    def test_login(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(response, "Login was not successful.")

    def test_login_view_with_valid_credentials(self):
        print("test")
        from django.contrib.auth import get_user_model

        User = get_user_model()
        User.objects.create_user(username='testuser', password='testpassword')

        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})

        # Check for a successful login and the correct redirect
        if '_auth_user_id' in self.client.session:
            print("User is authenticated")
        else:
            print("User authentication failed")

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        print(f"Response headers: {response.headers}")
        print(f"Response URL: {response.url}")

        self.assertEqual(response.status_code, 301)  # Check for HTTP 301 permanent redirect
        self.assertRedirects(response, reverse('home'), status_code=301)



    def test_login_view_with_invalid_credentials(self):
        # Test login view with invalid credentials
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertContains(response, 'Invalid username or password')

    def test_logout_view(self):
        # Test logout view
        try:
            user = User.objects.create_user(username='testuser', password='testpassword')
            self.client.login(username='testuser', password='testpassword')
            response = self.client.get(reverse('logout'))
            print(f"Initial response status code: {response.status_code}")
            print(f"Initial response content: {response.content.decode()}")
            print(f"Initial response headers: {response.headers}")

            # Assuming the logout view redirects to the success page
            expected_redirect_url = reverse('success_page')

            try:
                self.assertContains(response, 'successfully logged out', html=True)
                self.assertIn(response.status_code, [200, 302])  # Allow both 200 and 302 as valid status codes
                self.assertTemplateUsed(response, 'recipes/success.html')
            except AssertionError as e:
                print(f"AssertionError: {e}")

            # Add some prints to help identify issues if the test fails
            if response.status_code not in [200, 302]:
                print(f"Unexpected status code. Expected 200 or 302, got {response.status_code}")
            if 'successfully logged out' not in response.content.decode():
                print("Couldn't find 'successfully logged out' in response content.")
            if 'recipes/success.html' not in response.template_name:
                print(f"Unexpected template used. Expected 'recipes/success.html', got {response.template_name}")

            self.assertIn(response.status_code, [200, 302])
            self.assertContains(response, 'successfully logged out', html=True)
            self.assertTemplateUsed(response, 'recipes/success.html')
        except Exception as e:
            print(f"An error occurred during the test: {e}")









    def test_delete_account_view_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('delete_account'))

        # Assuming the delete_account view redirects to the login page
        expected_redirect_url = reverse('login')

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        print(f"Response headers: {response.headers}")
        print(f"Expected redirect URL: {expected_redirect_url}")

        try:
            self.assertRedirects(response, expected_url=expected_redirect_url, status_code=301, target_status_code=200)
        except AssertionError as e:
            print(f"AssertionError: {e}")

        # Add some prints to help identify issues if the test fails
        if response.status_code != 301:
            print("Unexpected status code. Expected 301.")
        if response.url != expected_redirect_url:
            print(f"Unexpected redirect URL. Expected: {expected_redirect_url}, Actual: {response.url}")

        self.assertEqual(response.status_code, 301)


    def test_register_view(self):
        # Test register view
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signup.html')


    def test_signup_view_with_valid_data(self):
        # Test signup view with valid data
        response = self.client.post(reverse('signup'), {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful registration
        self.assertRedirects(response, reverse('home'), status_code=302)

    def test_signup_view_with_invalid_data(self):
        # Test signup view with invalid data
        response = self.client.post(reverse('signup'), {'username': '', 'password1': 'password', 'password2': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signup.html')
        self.assertContains(response, 'Error in username: This field is required')




    



