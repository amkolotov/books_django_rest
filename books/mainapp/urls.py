from django.urls import path

from . import views

app_name = 'mainapp'

urlpatterns = [
    path('book/', views.BookListView.as_view()),
    path('book/<int:pk>/', views.BookDetailView.as_view()),
    path('review/', views.ReviewCreateView.as_view()),
    path('rating/', views.AddRatingView.as_view()),
    path('author/', views.AuthorListView.as_view()),
    path('author/<int:pk>/', views.AuthorDetailView.as_view())
]