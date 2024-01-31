# modules for file and random operations
import os
import random
# Import Django shortcuts for rendering, redirection, and user authentication
from django.shortcuts import render, redirect
from django.contrib.auth import logout
# Import Django's generic views for list and detail views
from django.views.generic import ListView, DetailView
# Import models and forms from the current application
from .models import Recipe
from .forms import RecipeForm 
# Import Django decorators for user authentication
from django.contrib.auth.decorators import login_required
# Import Django query objects for complex database queries
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin




# Define a view function named recipes_home that takes a request object as a parameter
def recipes_home(request):      
    all_images = Recipe.objects.filter(pic__isnull=False).exclude(pic='no_picture.jpeg').order_by('?')      # takes all pic objects, filters out the no-picture.jpg, and randomizes all objects--loads into the all_images object
    
    # Concatenate the list multiple times to ensure it's long enough for infinite scrolling
    random_images = list(all_images) * 100
    
    return render(request, 'recipes/recipes_home.html', {'random_images': random_images})

# defines search_view 
@login_required  
def search_view(request):
    query = request.GET.get('query', '')        # Get the 'query' parameter from the request's GET parameters; default to an empty string if not present
    
    # perform a case-insensitive search in the title and ingredients fields
    if query:       # If the query is not empty
        search_results = Recipe.objects.filter(
            Q(name__icontains=query) | Q(ingredients__icontains=query)      # icontains stands for "case-insensitive contains"--checks whether the specified substring is contained within the field's value, disregarding the case of the characters
        )
    # if the query is empty, search_results is set to an empty list
    else:
        search_results = []     
    # Render the 'recipes/search_results.html' template with the 'results' and 'query' variables in the context
    # using the information from the incoming HTTP request ('request' object).
    return render(request, 'recipes/search_results.html', {'results': search_results, 'query': query})

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
    # Add logic to delete the user and log them out
    user = request.user
    user.delete()
    return redirect('recipes:home')


class RecipeListView(LoginRequiredMixin, ListView):           #class-based “protected” view
    model = Recipe                         #specify model
    template_name = 'recipes/home.html'    #specify template
    context_object_name = 'object_list'     # the data that is passed to a template for rendering
    paginate_by = 10     # dictates how many instances are loaded per page

    def get_queryset(self):
        queryset = Recipe.objects.all().order_by('name')
        print(queryset.query)   # Print the generated SQL query
        return queryset     # Recipe.objects.all() retrieves all instances of the Recipe model, and .order_by('?')  orders them by name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_list = context['object_list']  # Update 'recipes' to 'object_list'

        paginator = Paginator(recipe_list, self.paginate_by)       # Create a paginator object for the recipe_list, paginating the recipe instances in the list view
        # Extract the value of the 'page' parameter from the GET request.
        # This is commonly used in paginated views to determine which page of content the user is currently viewing.
        page = self.request.GET.get('page')

        # Try to get the requested page of recipes from the paginator.
        # If the 'page' parameter is not an integer, default to the first page.
        # If the 'page' parameter is too high, default to the last page.
        try:
            recipes = paginator.page(page)
        except PageNotAnInteger:
            recipes = paginator.page(1)
        except EmptyPage:
            recipes = paginator.page(paginator.num_pages)

        context['object_list'] = recipes  # Update paginated recipes to 'object_list'
        return context      # returns updated context containing the paginated list

class RecipeDetailView(LoginRequiredMixin, DetailView):                       #class-based “protected” view
    model = Recipe                                        #specify model
    template_name = 'recipes/recipe_detail.html'                 #specify template
