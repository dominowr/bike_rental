from django.urls import path
from .views import (UserAccountView, DeleteServiceReservation, DeleteMotorcycleReservation,
                    UpdateMotorcycleReservationView, UpdateServiceReservationView)

app_name = 'user_account'
urlpatterns = [
    path('', UserAccountView.as_view(), name='index-account'),
    path(
        'service-reservation-delete/<int:pk>/', DeleteServiceReservation.as_view(), name='delete-service'
    ),
    path(
        'motorcycle-reservation-delete/<int:pk>/',
        DeleteMotorcycleReservation.as_view(), name='delete-motorcycle'
    ),
    path('update-motorcycle-reservation/<int:pk>/', UpdateMotorcycleReservationView.as_view(), name='update-motorcycle'),
    path('update-service-reservation/<int:pk>/', UpdateServiceReservationView.as_view(), name='update-service')
]
