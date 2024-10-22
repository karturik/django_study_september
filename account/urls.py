from django.urls import path, re_path, include
from . import views


urlpatterns = [
        path('', include('django.contrib.auth.urls')),
        path("register", views.register_request, name="register"),
        re_path(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
        
        path('signup', views.SignUpView.as_view(), name='signup'),
        path('validate_username', views.validate_username, name='validate_username'),

        path('contact-form/', views.contact_form, name='contact_form')
    ]