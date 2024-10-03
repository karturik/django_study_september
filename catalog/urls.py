from django.urls import path, re_path
from . import views


urlpatterns = [
        path('', views.catalog_main, name='catalog_main'),
        # re_path(r'^$', views.index, name='index'),
        re_path(r'^books/$', views.BookListView.as_view(), name='books_list'),
        re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors_list'),
        re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
        re_path(r'^author/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='author-detail'), # TODO Add view class
        re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
        re_path(r'^all_borrowed_books/$', views.LoanedBooksByAllListView.as_view(), name='all-borrowed'),
        re_path(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),

        re_path(r'^book/create/$', views.BookCreate.as_view(), name='book_create'),
        re_path(r'^book/(?P<pk>\d+)/update/$', views.BookUpdate.as_view(), name='book_update'),
        re_path(r'^book/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name='book_delete'),
    ]
