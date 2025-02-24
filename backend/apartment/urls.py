from django.urls import path
from .views import list_apartments, get_apartments_from_api

urlpatterns = [
    path('', list_apartments, name='list_apartments'),
    path('get-apartments/', get_apartments_from_api, name='get_apartments_from_api')
]