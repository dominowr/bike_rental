from .user_serializers.user_serializers import UserSerializer, UserRegistrationSerializer
from .rental_serializers.rental_serializers import (
    MotorcycleSerializer, MotorcycleCreateReservationSerializer, MotorcycleReservationSerializer,
    MotorcycleReservationListSerializer
    )
from .workshop_serializers.workshop_serializers import (
    ServiceSerializer, ServiceReservationSerializer, ServiceReservationListSerializer,
    ServiceCreateReservationSerializer
    )

