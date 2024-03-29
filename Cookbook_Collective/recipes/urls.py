from django.contrib import admin
from django.urls import include, path 
from django.conf.urls.static import static
from django.conf import settings

from recipe_project.views import login_view, logout_view, delete_account, signup

from .views import (
    recipes_home,
    search_view,
    RecipeListView,
    RecipeDetailView,
    create_recipe,
    RecipeListViewAll,
    recipe_type_distribution,
    recipe_difficulty_distribution,
    recipes_created_per_month,
    visualizations,
    credits2, 
    about_me,
)


app_name = 'recipes'

urlpatterns = [
    path('', recipes_home, name='home'),
    path('search/', search_view, name='search'),
    path('list/', RecipeListView.as_view(), name='recipe_list'),
    path('list/all/', RecipeListViewAll.as_view(), name='recipe_list_all'),
    path('list/<pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('create_recipe/', create_recipe, name='create_recipe'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('delete_account/', delete_account, name='delete_account'),
    path('credits2/', credits2, name='credits2'),
    path('signup/', signup, name='signup'),
    path('about_me/', about_me, name='about_me'),

    # Visualization URLs without a "visualizations" directory
    path('recipe-type-distribution/<str:type_of_recipe>/', recipe_type_distribution, name='recipe-type-distribution-detail'),
    path('recipe-type-distribution/', recipe_type_distribution, name='recipe-type-distribution'),
    path('recipe-difficulty-distribution/<str:type_of_recipe>/', recipe_difficulty_distribution, name='recipe-difficulty-distribution-detail'),
    path('recipe-difficulty-distribution/', recipe_difficulty_distribution, name='recipe-difficulty-distribution-default'),
    path('recipes-created-per-month/', recipes_created_per_month, name='recipes-created-per-month-detail'),
    path('visualizations/', visualizations, name='visualizations'),
]



# Specifies the URL “/media/” that will trigger this media view (in this case, an image)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
