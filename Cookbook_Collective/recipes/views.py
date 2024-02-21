# Standard Library
import os
import random
from io import BytesIO
import calendar
import pandas as pd
import matplotlib
import logging


# Django
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError, models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


# Third-party

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
    random_images = list(all_images) * 80
    context = {
        'loading': True,  # Set this to False when processing is complete
    }
    return render(request, 'recipes/recipes_home.html', {'random_images': random_images})

# test
@login_required
def search_view(request):
    form = SearchForm(request.GET or None)
    recipes_queryset = None

    if form.is_valid():
        query = form.cleaned_data['query'].strip()

        try:
            combined_query = models.Q(name__icontains=query) | models.Q(ingredients__icontains=query)
            recipes_queryset = Recipe.objects.filter(combined_query).order_by('name')

        except models.DatabaseError as e:
            messages.error(request, f"Error fetching recipes: {e}")

    paginator = Paginator(recipes_queryset or [], 10)
    page = request.GET.get('page', 1)

    try:
        recipes_paginated = paginator.page(page)
    except PageNotAnInteger:
        print(f"DEBUG: PageNotAnInteger - Using first page.")
        recipes_paginated = paginator.page(1)
    except EmptyPage:
        print(f"DEBUG: EmptyPage - Using last page.")
        recipes_paginated = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'recipes_queryset': recipes_paginated,
        'paginator': paginator,
    }

    return render(request, 'recipes/search_results.html', context)




# defines create_recipe view
@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                print("Form data before save:", form.cleaned_data) 
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



@login_required
def visualizations(request, type_of_recipe=None):
    recipes = None
    message = None

    if request.method == 'POST':
        selected_type = request.POST.get('type_of_recipe', '')
        if not selected_type:
            message = "Please select a type of recipe to proceed."
        else:
            try:
                # Handle the selected type, e.g., redirect to the detailed visualization page
                return redirect('recipes:recipe-difficulty-distribution-detail', type_of_recipe=selected_type)
            except ObjectDoesNotExist:
                # Handle the case when the queryset is empty
                message = "No recipes found for the selected type."
            except DatabaseError as e:
                # Handle other database query errors
                messages.error(request, f"Error fetching recipes: {e}")

    try:
        if type_of_recipe:
            recipes = Recipe.objects.filter(type_of_recipe=type_of_recipe)
        elif type_of_recipe is None:
            message = "Please select a type of recipe to proceed."
    except ObjectDoesNotExist:
        # Handle the case when the queryset is empty
        message = "No recipes found for the selected type."
    except DatabaseError as e:
        # Handle other database query errors
        messages.error(request, f"Error fetching recipes: {e}")

    context = {
        'type_of_recipe': type_of_recipe,
        'recipes': recipes,
        'message': message,
    }

    return render(request, 'recipes/visualizations.html', context)




    
# defines view for recipe_difficulty_distribution chart, taking the type of recipe as a parameter
@login_required
def recipe_difficulty_distribution(request, type_of_recipe=None):
    chart_image = None

    try:
        data = get_recipe_difficulty_distribution_data(request, type_of_recipe)
        print("Data for Difficulty Distribution Chart:", data)
        chart_image = render_chart(request, chart_type=2, data=data)
    except Exception as e:
        messages.error(request, f"Error rendering difficulty distribution chart: {e}")

    context = {
        'chart_image': chart_image,
        'description': "Recipe Difficulty Distribution",
    }
    return render(request, 'recipes/recipe_difficulty_distribution.html', context)




# defines view for recipe_type_distribution chart on all recipes
@login_required
def recipe_type_distribution(request, type_of_recipe=None):
    try:
        if not type_of_recipe:
            type_of_recipe = 'default'
        data = get_recipe_type_distribution_data(type_of_recipe)
        chart_image = render_chart(request, chart_type=1, data=data)
    except Exception as e:
        # Handle unexpected errors during chart rendering
        messages.error(request, f"Error rendering type distribution chart: {e}")
        chart_image = None

    return render(request, 'recipes/recipe_type_distribution.html', {'chart_image': chart_image})


@login_required
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

def credits2(request):
    return render(request, 'recipes/credits2.html')



class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html' 
    context_object_name = 'object_list'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        print("get method called")
        print("Paginate by:", self.paginate_by)
        response = super().get(request, *args, **kwargs)
        return response

    def get_queryset(self):
        print("get_queryset method called")
        distinct_names = Recipe.objects.values('name').distinct()
        queryset = Recipe.objects.filter(name__in=distinct_names).order_by('name')
        return queryset




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context['paginator']
        recipe_list = context['page_obj']

        context['object_list'] = recipe_list
        context['paginator'] = paginator

        return context





class RecipeDetailView(LoginRequiredMixin, DetailView):                       #class-based “protected” view
    model = Recipe                                        #specify model
    template_name = 'recipes/recipe_detail.html'                 #specify template


# uses a list view to view all recipes
class RecipeListViewAll(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html' 
    context_object_name = 'object_list_all'
    paginate_by = 10

    def get_queryset(self):
        return Recipe.objects.all().order_by('name')




