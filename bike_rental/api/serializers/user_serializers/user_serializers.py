from rest_framework import serializers
from django.contrib.auth import get_user_model
from rental.models.motorcycle_reservation_model import MotorcycleReservation
from workshop.models.service_reservation_model import ServiceReservation
from authentication.forms.utils import PasswordValidator


class UserSerializer(serializers.ModelSerializer):
    motorcyclereservation_set = serializers.PrimaryKeyRelatedField(
        many=True, queryset=MotorcycleReservation.objects.all(),
    )

    servicereservation_set = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ServiceReservation.objects.all(),
    )

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'first_name', 'email', 'motorcyclereservation_set', 'servicereservation_set'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'username', 'first_name', 'last_name', 'phone_no', 'email', 'password', 'password2',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data.get('email')

        if self.Meta.model.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                PasswordValidator.error_messages['email_used'],
                code='email_used',
            )

        password = data.get('password')
        PasswordValidator.clean_password(password)

        password2 = data.get('password2')
        PasswordValidator.clean_password2(password, password2)

        return data


