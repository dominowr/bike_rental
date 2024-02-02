from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, time
from django.contrib.auth import get_user_model
from workshop.models import Service, ServiceReservation


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price']


class ServiceReservationSerializer(serializers.ModelSerializer):
    """
    Displays list of reservations with all data for superuser.
    """
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = ServiceReservation
        fields = ['id', 'user', 'service', 'date_time']


class ServiceReservationListSerializer(serializers.ModelSerializer):
    """
    Displays reservation list of reservations fo unauthenticated user and for specific user.
    """
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    class Meta:
        model = ServiceReservation
        fields = ['id', 'service', 'date_time']


class ServiceCreateReservationSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    date = serializers.DateField(write_only=True)
    hour = serializers.CharField(write_only=True)
    date_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ServiceReservation
        fields = ['service', 'date', 'hour', 'date_time']

    def validate(self, data):
        date = data.get('date')
        hour = data.get('hour')

        current_date = datetime.now().date()
        open_hour = time(7, 0)
        close_hour = time(16, 0)

        try:
            selected_date = timezone.make_aware(
                datetime.strptime(f'{date} {hour}', '%Y-%m-%d %I:%M %p')
            )
            if selected_date.date() >= current_date and open_hour <= selected_date.time() <= close_hour:
                data['date_time'] = selected_date
                return data
            else:
                raise serializers.ValidationError('Sorry, we are closed.')
        except ValueError:
            raise serializers.ValidationError('Invalid date or time format.')
