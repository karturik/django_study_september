from django.urls import path
import views


urlpatterns = [
        path('', views.catalog_main, name='catalog_main'),
    ]
