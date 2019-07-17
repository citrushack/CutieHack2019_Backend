from django.conf.urls import url
from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('email/', views.email, name='email'),
        path('success/', views.success, name='success'),
        path('signup/', views.signup, name='signup'),
        path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),
]
