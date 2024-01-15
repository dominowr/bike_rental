from django.urls import path
from .views import WorkshopIndexView, ServiceDetailView, CreateWorkshopReservation


app_name = 'workshop'
urlpatterns = [
    path('', WorkshopIndexView.as_view(), name='index-workshop'),
    path('service/<slug:slug>/', ServiceDetailView.as_view(), name='service-workshop'),
    path('set/workshop-reservation/', CreateWorkshopReservation.as_view(), name='set-reservation'),
]
