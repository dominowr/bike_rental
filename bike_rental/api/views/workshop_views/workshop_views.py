from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from workshop.models import Service, ServiceReservation
from workshop.views.utils import get_unavailable_hours, send_confirmation_mail
from api import serializers
from api.views.permission import IsSuperUser


class ServiceList(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class ServiceAdd(generics.CreateAPIView):
    permission_classes = [IsSuperUser]
    serializer_class = serializers.ServiceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceReservationList(generics.ListAPIView):
    serializer_class = serializers.ServiceReservationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return ServiceReservation.objects.all()
            else:
                return ServiceReservation.objects.filter(user=user)
        else:
            return ServiceReservation.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return self.serializer_class
            else:
                return serializers.ServiceReservationListSerializer
        else:
            return serializers.ServiceReservationListSerializer


class ServiceCreateReservation(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ServiceCreateReservationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            service = get_object_or_404(
                Service, name=serializer.validated_data['service']
            )
            unavailable_hours = get_unavailable_hours(service.slug)
            selected_date = serializer.validated_data['date']
            selected_time = serializer.validated_data['hour']
            date_time = serializer.validated_data['date_time']

            if selected_date in unavailable_hours and selected_time in unavailable_hours[selected_date]:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.validated_data.pop('date')
            serializer.validated_data.pop('hour')

            serializer.save(user=request.user, date_time=date_time)

            send_confirmation_mail(request.user, service, selected_date, selected_time)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDeleteReservation(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ServiceReservationListSerializer

    def get_queryset(self):
        user = self.request.user
        return ServiceReservation.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
