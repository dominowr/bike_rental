from datetime import datetime
from dateutil import parser
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rental.models import Motorcycle, MotorcycleReservation


class MotorcycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorcycle
        fields = '__all__'


class MotorcycleReservationSerializer(serializers.ModelSerializer):
    """
    Displays list of reservations with all data for superuser.
    """
    motorcycle = serializers.PrimaryKeyRelatedField(queryset=Motorcycle.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = MotorcycleReservation
        fields = '__all__'


class MotorcycleReservationListSerializer(serializers.ModelSerializer):
    """
    Displays reservation list of reservations fo unauthenticated user and for specific user.
    """
    motorcycle = serializers.PrimaryKeyRelatedField(queryset=Motorcycle.objects.all())

    class Meta:
        model = MotorcycleReservation
        fields = ['id', 'motorcycle', 'start_date', 'end_date']


class MotorcycleCreateReservationSerializer(serializers.ModelSerializer):
    motorcycle = serializers.PrimaryKeyRelatedField(queryset=Motorcycle.objects.all())

    class Meta:
        model = MotorcycleReservation
        fields = ['motorcycle', 'start_date', 'end_date']

    def validate(self, data):
        full_data = self.initial_data
        current_date = datetime.now().date()
        try:
            start_date = parser.parse(full_data.get('start_date')).date()
            end_date = parser.parse(full_data.get('end_date')).date()

            if start_date >= current_date and end_date >= current_date and not end_date < start_date:
                return data
            else:
                raise serializers.ValidationError('Invalid data.')
        except ValueError:
            raise serializers.ValidationError('Invalid data.')
