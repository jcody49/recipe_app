# modules for file and random operations
import os
import random
# Import Django shortcuts for rendering, redirection, and user authentication
from django.shortcuts import render, redirect
from django.contrib.auth import logout
# Import Django's generic views for list and detail views
from django.views.generic import ListView, DetailView
# Import models and forms from the current application
from .models import Recipe, TYPE_OF_RECIPE
from .forms import RecipeForm, SearchForm 
# Import Django decorators for user authentication
from django.contrib.auth.decorators import login_required
# Import Django query objects for complex database queries
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
from .utils import get_recipe_name_from_id
import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.http import HttpResponse
from .models import DIFFICULTY_LEVELS
from django.db.models import Count
import calendar
from .utils import render_chart, get_recipe_type_distribution_data, get_recipe_difficulty_distribution_data, get_recipe_name_from_id
import numpy as np

# django's logger--helps with debugging
logger = logging.getLogger(__name__)


# Define a view function named recipes_home that takes a request object as a parameter
def recipes_home(request):      
    all_images = Recipe.objects.filter(pic__isnull=False).exclude(pic='no_picture.jpeg').order_by('?')      # takes all pic objects, filters out the no-picture.jpg, and randomizes all objects--loads into the all_images object
    
    # Concatenate the list multiple times to ensure it's long enough for infinite scrolling
    random_images = list(all_images) * 100
    
    return render(request, 'recipes/recipes_home.html', {'random_images': random_images})


@login_required
def search_view(request):
    form = SearchForm(request.GET or None)      # applies the SearchForm class to a form that is intende to use the GET method
    recipes_queryset = None     # initializes the recipe's query set to none

    if form.is_valid():
        query = form.cleaned_data['query'].strip()      # strips the whitespace from the query

        if query:
            # Use Q objects to combine queries for name and ingredients
            combined_query = Q(name__icontains=query) | Q(ingredients__icontains=query)

            # Filter recipes based on the combined query
            recipes_queryset = Recipe.objects.filter(combined_query)

    # The context dictionary is passed as an argument to a Django template renderer, allowing the template to access and display the values associated with the keys
    context = {
        'form': form,
        'recipes_queryset': recipes_queryset,
    }

    return render(request, 'recipes/search_results.html', context)



# defines create_recipe view
@login_required
def create_recipe(request):
    if request.method == 'POST':        # checks if req is POST
        form = RecipeForm(request.POST, request.FILES)      # Takes input from a form and sends it as a POST req, which in Django, is handled by creating an instance of the RecipeForm class--This line creates a new instance of the RecipeForm class and initializes it with the data from the user's submitted form
        if form.is_valid():     # checks validity of data
            recipe = form.save(commit=False)        # Save the form data to a Recipe object without committing to the database
            recipe.calculate_difficulty()       # Calculate difficulty before saving
            recipe.save()
            return redirect('recipes:recipe_detail', pk=recipe.pk)      # upon creation, user is redirected to the recipe_detail view to see their newly created recipe object using its primary key.
    else:
        form = RecipeForm()     # if the request type is invalid, an empty instance of RecipeForm is created

    return render(request, 'recipes/create_recipe.html', {'form': form})        # Render the create_recipe.html template with the form instance in the context (the data that is passed to a template for rendering)

@login_required     # restricts access to only authenticated users
def delete_account(request):
    # logic to delete the user and log them out
    user = request.user
    user.delete()
    return redirect('recipes:home')


def visualizations(request, type_of_recipe=None):
    
    

    # Fetch recipes based on type_of_recipe, adjust this part as needed
    if type_of_recipe:
        recipes = Recipe.objects.filter(type_of_recipe=type_of_recipe)
    else:
        recipes = None  # You may want to fetch all recipes or leave it as None if not needed

    # Check if type_of_recipe is None and set a message
    if type_of_recipe is None:
        message = "Please select a type of recipe to proceed."
    else:
        message = None

    context = {
        'type_of_recipe': type_of_recipe,
        'recipes': recipes,
        'message': message,  # Include the message in the context
    }
    return render(request, 'recipes/visualizations.html', context)



    
# defines view for recipe_difficulty_distribution chart, taking the type of recipe as a parameter
def recipe_difficulty_distribution(request, type_of_recipe):
    data = get_recipe_difficulty_distribution_data(type_of_recipe)      # calls the function to get the required data for the chart
    chart_image = render_chart(request, chart_type=2, data=data)  # Use chart_type 2 with the data just gathered to produce a chart_image

    context = {
        'chart_image': chart_image,
        'description': "Recipe Difficulty Distribution",
    }
    return render(request, 'recipes/recipe_difficulty_distribution.html', context)

# defines view for recipe_type_distribution chart on all recipes
def recipe_type_distribution(request, type_of_recipe=None):
    # If type_of_recipe is not specified, get data for all recipe types
    if type_of_recipe is None:
        data = get_recipe_type_distribution_data()
    else:
        # Get data for a specific recipe type
        data = get_recipe_type_distribution_data(type_of_recipe)

    chart_image = render_chart(request, chart_type=1, data=data)

    return render(request, 'recipes/recipe_type_distribution.html', {'chart_image': chart_image})



def recipes_created_per_month(request):
    # Generate made-up data for demonstration
    months = [calendar.month_name[i] for i in range(1, 13)]
    recipes_created = [10, 15, 20, 25, 30, 35, 40, 45, 50, 45, 40, 35]

    # Convert the data to a Pandas DataFrame
    data = pd.DataFrame({"month": months, "recipe_count": recipes_created})

    # Render the chart using your existing render_chart function
    chart_image = render_chart(request, chart_type=3, data=data)

    # Provide any additional context or description needed for your template
    context = {
        'chart_image': chart_image,
        'description': "Visualize the number of recipes created per month. This chart provides insights into the monthly growth of your recipe collection."
    }

    # Render the template for recipes created per month
    return render(request, 'recipes/recipes_created_per_month.html', context)

class RecipeListView(LoginRequiredMixin, ListView):           #class-based “protected” view
    model = Recipe                         #specify model
    template_name = 'recipes/home.html'    #specify template
    context_object_name = 'object_list'     # the data that is passed to a template for rendering
    paginate_by = 10     # dictates how many instances are loaded per page

    def get_queryset(self):
        queryset = Recipe.objects.all().order_by('name')
        return queryset     # Recipe.objects.all() retrieves all instances of the Recipe model, and .order_by('?')  orders them by name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_list = context['object_list']  # Update 'object_list_all' to 'object_list'

        paginator = Paginator(recipe_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            recipes = paginator.page(page)
        except PageNotAnInteger:
            recipes = paginator.page(1)
        except EmptyPage:
            recipes = paginator.page(paginator.num_pages)

        context['object_list'] = recipes  # Update paginated recipes to 'object_list'
        return context



class RecipeDetailView(LoginRequiredMixin, DetailView):                       #class-based “protected” view
    model = Recipe                                        #specify model
    template_name = 'recipes/recipe_detail.html'                 #specify template

# uses a list view to view all recipes
class RecipeListViewAll(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'object_list_all'
    paginate_by = 10

    def get_queryset(self):
        return Recipe.objects.all().order_by('name')




