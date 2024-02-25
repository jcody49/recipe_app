
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from django.conf.urls.static import static
from django.conf import settings
from recipes.views import recipes_home
from .views import login_view, logout_view, signup, delete_account
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', recipes_home, name='home'),
    path('', include('recipes.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('delete_account/', delete_account, name='delete_account'),
    path('docs/', include('recipe_project.docs_urls')),
]

# specifies the URL “/media/” that will trigger this media view (in this case, an image)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
