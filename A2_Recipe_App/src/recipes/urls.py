from django.contrib import admin
from django.urls import include, path
from recipes.views import recipes_home  
from .views import RecipeListView

# test
from recipes.views import (
    recipes_home,
    search_view,
    RecipeListView,
    RecipeDetailView,
    create_recipe,
    logout_view, 
    delete_account,
)
from django.conf.urls.static import static
from django.conf import settings

app_name = 'recipes'

urlpatterns = [
    path('', recipes_home, name='home'),
    path('search/', search_view, name='search'),
    path('list/', RecipeListView.as_view(), name='recipe_list'),   
    path('list/<pk>', RecipeDetailView.as_view(), name='recipe_detail'),     
    path('create_recipe/', create_recipe, name='create_recipe'), 
    path('logout/', logout_view, name='logout'),
    path('delete_account/', delete_account, name='delete_account'),
]

# specifies the URL “/media/” that will trigger this media view (in this case, an image)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)