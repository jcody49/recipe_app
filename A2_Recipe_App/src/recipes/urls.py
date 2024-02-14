from django.contrib import admin
from django.urls import include, path 
from django.conf.urls.static import static
from django.conf import settings

from .views import RecipeListView, render_chart  
from recipe_project.views import login_view 

from .views import (
    recipes_home,
    search_view,
    RecipeListView,
    RecipeDetailView,
    create_recipe,
    delete_account,
    RecipeListViewAll,
    recipe_type_distribution,
    recipe_difficulty_distribution,
    recipes_created_per_month,
    visualizations,
)


app_name = 'recipes'

urlpatterns = [
    path('', recipes_home, name='home'),
    path('search/', search_view, name='search'),
    path('list/', RecipeListView.as_view(), name='recipe_list'),
    path('list/all/', RecipeListViewAll.as_view(), name='recipe_list_all'),  # Add this line for showing all recipes
    path('list/<pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('create_recipe/', create_recipe, name='create_recipe'),
    path('delete_account/', delete_account, name='delete_account'),
    path('login/', login_view, name='login'),
    # Visualization URLs without a "visualizations" directory
    path('recipe-type-distribution/<type_of_recipe>/', recipe_type_distribution, name='recipe_type_distribution_detail'),
    path('recipe-type-distribution/', recipe_type_distribution, name='recipe_type_distribution'),
    path('recipe_difficulty_distribution/<str:type_of_recipe>/', recipe_difficulty_distribution, name='recipe_difficulty_distribution'),
    path('recipes_created_per_month/', recipes_created_per_month, name='recipes_created_per_month'),
    path('visualizations/', visualizations, name='visualizations'),
    path('recipe-type-distribution/<str:type_of_recipe>/', recipe_type_distribution, name='recipe_type_distribution_detail'),
    path('recipe-difficulty-distribution/<str:type_of_recipe>/', recipe_difficulty_distribution, name='recipe_difficulty_distribution'),
    path('recipes-created-per-month/', recipes_created_per_month, name='recipes_created_per_month'),
]


# Specifies the URL “/media/” that will trigger this media view (in this case, an image)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
