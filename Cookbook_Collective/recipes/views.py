# Standard Library
import os
import random
from io import BytesIO
import calendar

# Django
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

# Third-party
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Project-specific
from .models import Recipe, TYPE_OF_RECIPE, DIFFICULTY_LEVELS
from .forms import RecipeForm, SearchForm
from .utils import (
    get_recipe_name_from_id, render_chart,
    get_recipe_type_distribution_data, get_recipe_difficulty_distribution_data
)




# Define a view function named recipes_home that takes a request object as a parameter
def recipes_home(request):      
    all_images = Recipe.objects.filter(pic__isnull=False).exclude(pic='no_picture.jpeg').order_by('?')      # takes all pic objects, filters out the no-picture.jpg, and randomizes all objects--loads into the all_images object
    
    # Concatenate the list multiple times to ensure it's long enough for infinite scrolling
    random_images = list(all_images) * 100
    
    return render(request, 'recipes/recipes_home.html', {'random_images': random_images})


@login_required
def search_view(request):
    form = SearchForm(request.GET or None)
    recipes_queryset = None

    if form.is_valid():
        query = form.cleaned_data['query'].strip()

        try:
            combined_query = Q(name__icontains=query) | Q(ingredients__icontains=query)
            recipes_queryset = Recipe.objects.filter(combined_query)
        except DatabaseError as e:
            # Handle database query error
            messages.error(request, f"Error fetching recipes: {e}")

    context = {
        'form': form,
        'recipes_queryset': recipes_queryset,
    }

    return render(request, 'recipes/search_results.html', context)



# defines create_recipe view
@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                print("Form data before save:", form.cleaned_data)  # Add this print statement
                recipe = form.save(commit=False)
                recipe.calculate_difficulty()
                recipe.save()

                # Display a success message
                messages.success(request, "Recipe created successfully!")

                return redirect('recipes:recipe_detail', pk=recipe.pk)
            except Exception as e:
                # Handle unexpected errors during recipe creation
                print(f"Error creating recipe: {e}")
                messages.error(request, f"Error creating recipe: {e}")
        else:
            # Invalid form data, display an error message
            print("Invalid form data. Form errors:", form.errors)
            messages.error(request, "Invalid form data. Please check your input.")
    else:
        form = RecipeForm()

    return render(request, 'recipes/create_recipe.html', {'form': form})




def visualizations(request, type_of_recipe=None):
    if type_of_recipe:
        try:
            recipes = Recipe.objects.filter(type_of_recipe=type_of_recipe)
        except DatabaseError as e:
            # Handle database query error
            messages.error(request, f"Error fetching recipes: {e}")
            recipes = None
    else:
        recipes = None

    if type_of_recipe is None:
        message = "Please select a type of recipe to proceed."
    else:
        message = None

    context = {
        'type_of_recipe': type_of_recipe,
        'recipes': recipes,
        'message': message,
    }
    return render(request, 'recipes/visualizations.html', context)




    
# defines view for recipe_difficulty_distribution chart, taking the type of recipe as a parameter
def recipe_difficulty_distribution(request, type_of_recipe):
    try:
        data = get_recipe_difficulty_distribution_data(type_of_recipe)
        chart_image = render_chart(request, chart_type=2, data=data)
    except Exception as e:
        # Handle unexpected errors during chart rendering
        messages.error(request, f"Error rendering difficulty distribution chart: {e}")
        chart_image = None

    context = {
        'chart_image': chart_image,
        'description': "Recipe Difficulty Distribution",
    }
    return render(request, 'recipes/recipe_difficulty_distribution.html', context)


# defines view for recipe_type_distribution chart on all recipes
def recipe_type_distribution(request, type_of_recipe=None):
    try:
        if type_of_recipe is None:
            data = get_recipe_type_distribution_data()
        else:
            data = get_recipe_type_distribution_data(type_of_recipe)
        chart_image = render_chart(request, chart_type=1, data=data)
    except Exception as e:
        # Handle unexpected errors during chart rendering
        messages.error(request, f"Error rendering type distribution chart: {e}")
        chart_image = None

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

# test
class RecipeListView(LoginRequiredMixin, ListView):           #class-based “protected” view
    model = Recipe                         #specify model
    template_name = 'recipes/home.html'    #specify template
    context_object_name = 'object_list'     # the data that is passed to a template for rendering
    paginate_by = 10     # dictates how many instances are loaded per page

    def get_queryset(self):
        distinct_names = Recipe.objects.values('name').distinct()
        queryset = Recipe.objects.filter(name__in=distinct_names).order_by('name')
        return queryset
        
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




