from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register_page, name='register'),
    path('accounts/login/', login_page, name='login'),
    path('logout/', logout, name='logout')
]