from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from config.views import home



urlpatterns = [
    re_path(r"^$|^\/$|^home\/$",home,name="home"),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('users/', include('apps.users.urls')),
    path('movies/', include('apps.movies.urls')),
    path('reviews/', include('apps.reviews.urls')),
    # path('recommendations/', include('apps.recommendations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
