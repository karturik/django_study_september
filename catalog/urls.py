from django.urls import path, re_path
from . import views


urlpatterns = [
        path('', views.catalog_main, name='catalog_main'),
        # re_path(r'^$', views.index, name='index'),
        re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    ]
