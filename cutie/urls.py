from django.contrib import admin
from django.urls import path
from .views import emailView, successView, index

urlpatterns = [
        path('', index, name='index'),
        path('email/', emailView, name='email'),
        path('success/', successView, name='success'),
]

