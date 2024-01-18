from django.shortcuts import render
from .models import Recipe

# takes the request coming from the web application and returns the template available at sales/home.html as a response
def recipes_home(request):
    return render(request, 'recipes/recipes_home.html')
