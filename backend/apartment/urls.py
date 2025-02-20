from django.urls import path
from .views import list_apartments

urlpatterns = [
    path('', list_apartments, name='list_apartments'),
]