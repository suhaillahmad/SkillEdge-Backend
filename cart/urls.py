from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('create_cart/', createcart.as_view(), name='add_to_cart'),
    path('cartid/', cartid.as_view(), name='cartid'),
    path('viewcart/', viewcart.as_view(), name='viewcart'),
    path('add_to_cart/<int:ck>/', cartadd.as_view(), name='add_to_cart'),
    path('remove_from_cart/<str:ck>/', cartremove.as_view(), name='remove_from_cart'),
]