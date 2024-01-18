from django.contrib import admin
from django.urls import include, path
from recipes.views import recipes_home  

urlpatterns = [
    path('', recipes_home, name='home'),
    
]
