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

    def test_delete_account_view_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

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
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next={}'.format(reverse('recipes:visualizations')), status_code=302)
        
 




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
        self.assertFalse(data.empty)
        self.assertIn('difficulty', data.columns)
        self.assertIn('count', data.columns)

        # Test when there is no data available
        data = get_recipe_difficulty_distribution_data(request=None, type_of_recipe='invalid_type')
        self.assertTrue(data.empty)

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
            # Test login view with valid credentials
            User.objects.create_user(username='testuser', password='testpassword')
            response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
            self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful login
            self.assertRedirects(response, reverse('home'), status_code=302)

        def test_login_view_with_invalid_credentials(self):
            # Test login view with invalid credentials
            response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'auth/login.html')
            self.assertContains(response, 'Invalid username or password')

        def test_logout_view(self):
            # Test logout view
            user = User.objects.create_user(username='testuser', password='testpassword')
            self.client.login(username='testuser', password='testpassword')
            response = self.client.get(reverse('logout'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'recipes/success.html')
            self.assertContains(response, 'You\'ve successfully logged out.')

        def test_delete_account_view_authenticated(self):
            # Test delete account view when authenticated
            user = User.objects.create_user(username='testuser', password='testpassword')
            self.client.login(username='testuser', password='testpassword')
            response = self.client.get(reverse('delete_account'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'auth/delete_account.html')

        def test_register_view(self):
            # Test register view
            response = self.client.get(reverse('register'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'auth/register.html')

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




        



