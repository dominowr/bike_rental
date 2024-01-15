from django.urls import path
from .views import FilterView, BikeDetailView, CreateMotorcycleReservation

app_name = 'rental'
urlpatterns = [
    path('', FilterView.as_view(), name='index-rental'),
    path('filter/<slug:slug>/', FilterView.as_view(), name='category-filter'),
    path('offer/<slug:slug>/', BikeDetailView.as_view(), name='bike-detail'),
    path('create/bike-reservation/', CreateMotorcycleReservation.as_view(), name='create-reservation'),
]
