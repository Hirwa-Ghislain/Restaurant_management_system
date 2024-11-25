# reservations/urls.py
from django.urls import path
from .views import view_available_reservations,make_reservation,view_customer_reservations

urlpatterns = [
    path('view/', view_available_reservations, name='view_reservations'),
    path('make/', make_reservation, name='make_reservation'),
    path('reservations/', view_customer_reservations, name='view_customer_reservations'),
]
