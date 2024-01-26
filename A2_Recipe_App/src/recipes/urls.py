from django.contrib import admin
from django.urls import include, path
from recipes.views import recipes_home  
from .views import search_view
from django.conf.urls.static import static
from django.conf import settings

# test 3
urlpatterns = [
    path('', recipes_home, name='home'),
    path('search/', search_view, name='search'),
    
]

# specifies the URL “/media/” that will trigger this media view (in this case, an image)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)