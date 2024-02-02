from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('users/', views.UserList.as_view()), #done
    path('users/registration/', views.UserRegister.as_view()),  #done
    path('motorcycles/', views.MotorcycleList.as_view()), #done
    path('motorcycles/add/', views.MotorcycleAdd.as_view()),
    path('motorcycles-reservations/', views.MotorcycleReservationList.as_view()), #done
    path('motorcycles-reservations/add/', views.MotorcycleCreateReservation.as_view()),
    path('motorcycles-reservations/delete/<int:pk>/', views.MotorcycleDeleteReservation.as_view()),
    path('services/', views.ServiceList.as_view()), #done
    path('services/add/', views.ServiceAdd.as_view()),
    path('services-reservations/', views.ServiceReservationList.as_view()), #done
    path('services-reservations/add/', views.ServiceCreateReservation.as_view()),
    path('services-reservations/delete/<int:pk>/', views.ServiceDeleteReservation.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += [
    path('api-auth/', include('rest_framework.urls'))
]
urlpatterns += [
    path('api-token-auth/', views.UserAuthToken.as_view())
]
