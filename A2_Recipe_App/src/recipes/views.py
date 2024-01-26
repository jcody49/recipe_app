import os
from django.shortcuts import render
from .models import Recipe
import random



def recipes_home(request):
    all_images = Recipe.objects.filter(pic__isnull=False).exclude(pic='no_picture.jpeg').order_by('?')
    
    # Concatenate the list multiple times to ensure it's long enough for infinite scrolling
    random_images = list(all_images) * 100
    
    return render(request, 'recipes/recipes_home.html', {'random_images': random_images})

   
def search_view(request):
    query = request.GET.get('query', '')
    
    # If the query is not empty, perform a case-insensitive search in the title field
    if query:
        search_results = Recipe.objects.filter(name__icontains=query)
    else:
        search_results = []

    return render(request, 'recipes/search_results.html', {'results': search_results, 'query': query})
