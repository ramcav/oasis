from django.urls import path
from .views import (
    list_cleanings, create_cleaning, get_cleaning, update_cleaning,
    list_reviews, get_review, create_review, update_review, delete_review
)

urlpatterns = [
    path('', list_cleanings, name='list_cleanings'),
    path('create/', create_cleaning, name='create_cleaning'),
    path('<int:pk>/', get_cleaning, name='get_cleaning'),
    path('<int:pk>/update/', update_cleaning, name='update_cleaning'),
    
    path('reviews/', list_reviews, name='list_reviews'),
    path('reviews/<int:pk>/', get_review, name='get_review'),
    path('reviews/create/', create_review, name='create_review'),
    path('reviews/<int:pk>/update/', update_review, name='update_review'),
    path('reviews/<int:pk>/delete/', delete_review, name='delete_review'),
]