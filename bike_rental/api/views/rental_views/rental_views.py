import pandas as pd
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rental.models import Motorcycle, MotorcycleReservation
from rental.views.utils import get_unavailable_dates, send_confirmation_mail
from api import serializers
from api.views.permission import IsSuperUser


class MotorcycleList(generics.ListAPIView):
    queryset = Motorcycle.objects.all()
    serializer_class = serializers.MotorcycleSerializer


class MotorcycleAdd(generics.CreateAPIView):
    permission_classes = [IsSuperUser]
    serializer_class = serializers.MotorcycleSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            instance = serializer.save()
            instance.refresh_from_db()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MotorcycleReservationList(generics.ListAPIView):
    serializer_class = serializers.MotorcycleReservationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            if user.is_superuser:
                return MotorcycleReservation.objects.all()
            else:
                return MotorcycleReservation.objects.filter(user=user)
        else:
            return MotorcycleReservation.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return self.serializer_class
            else:
                return serializers.MotorcycleReservationListSerializer
        else:
            return serializers.MotorcycleReservationListSerializer


class MotorcycleCreateReservation(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MotorcycleCreateReservationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            motorcycle = get_object_or_404(
                Motorcycle, model=serializer.validated_data['motorcycle']
            )
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']

            date_range = pd.date_range(start_date, end_date).strftime('%Y-%m-%d')

            unavailable_dates = get_unavailable_dates(motorcycle)

            if any(date in unavailable_dates for date in date_range):
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(user=request.user, motorcycle=motorcycle)
            send_confirmation_mail(request.user, motorcycle, start_date, end_date, date_range)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MotorcycleDeleteReservation(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MotorcycleReservationSerializer

    def get_queryset(self):
        user = self.request.user
        return MotorcycleReservation.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

