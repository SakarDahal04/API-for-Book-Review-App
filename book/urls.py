from django.urls import path
from book import views

urlpatterns = [
    path('', views.BookListAPIView.as_view(), name='book-list'),
    path('create/', views.BookCreateAPIView.as_view(), name='book-create'),
    path('<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
    path('user/<int:pk>/', views.UserBookAPIView.as_view(), name='user-books'),
    path('book-delete/<int:pk>/', views.UserBookDeleteAPIView.as_view(), name='book-delete'),
    path('review-create/<int:book_id>/', views.ReviewCreateAPIView.as_view(), name='review-create'),
    path('review-delete/<int:pk>/', views.ReviewDeleteAPIView.as_view(), name='review-delete'),

]
