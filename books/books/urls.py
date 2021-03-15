"""books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as doc_urls
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api-auth/', include('rest_framework.urls', namespace='rest')),
#     path('auth/', include('djoser.urls')),
#     path('auth/', include('djoser.urls.authtoken')),
#     path('auth/', include('djoser.urls.jwt')),
#
#     path('api/v1/', include('mainapp.urls', namespace='main')),
# ]

# for deploy docker with vue
urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/auth/', include('djoser.urls.jwt')),

    path('api/v1/', include('mainapp.urls', namespace='main')),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
