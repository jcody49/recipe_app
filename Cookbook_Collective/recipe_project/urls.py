from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from recipes.views import recipes_home, visualizations, recipe_difficulty_distribution, recipe_difficulty_distribution_default
from .views import login_view, logout_view, signup, delete_account, credits

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('delete_account/', delete_account, name='delete_account'),
    path('recipe_difficulty_distribution/<str:type_of_recipe>/', recipe_difficulty_distribution, name='recipe_difficulty_distribution_detail'),
    path('recipe_difficulty_distribution/', recipe_difficulty_distribution_default, name='recipe_difficulty_distribution_default'),  # Modify this line
    path('credits/', credits, name='credits'),
]

# specifies the URL “/media/” that will trigger this media view (in this case, an image)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
