# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/', views.recommend_by_favorites, name='recommend_by_favorites'),
    path('book-suggest/', views.book_suggest, name='book-suggest'),
    path('search/', views.search_books, name='search_books'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('random/', views.random_book, name='random_book'),
]
