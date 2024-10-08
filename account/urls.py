from django.urls import path, re_path, include
from . import views


urlpatterns = [
        path('', include('django.contrib.auth.urls')),
        path("register", views.register_request, name="register"),
        re_path(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
    ]