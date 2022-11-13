"""bookapirest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from apibook import models as api_models
from apibook import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apibook.urls')),
    path("api-auth/", include('rest_framework.urls')),
    path("api/v1/rest-auth/", include('dj_rest_auth.urls')),
    path('api/v1/rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # empty view to fix issues error reverse  password_reset_confirm' not found
    path('password-reset/<uidb64>/<token>/', 
         api_views.Empty_view, name='password_reset_confirm'),
    path("api/v1/dispos/<str:d_start>/", api_views.JsonDataSelect.as_view(),  name="calendar_slot")

]
