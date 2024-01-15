from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import IntegrityError
from .workshop_factory import UserFactory, ServiceFactory, ServiceImagesFactory, ReservationFactory
from workshop.models import Service, ServiceReservation, ServiceImages
from authentication.models import User


class TestServiceModel(TestCase):
    def setUp(self) -> None:
        self.service_set = ServiceFactory.create_batch(5)
        self.service_images_set = [ServiceImagesFactory(service=service) for service in self.service_set]
        # self.service_images_set = []

    def test_get_and_str_method(self):
        for service in self.service_set:
            service_db = Service.objects.get(pk=service.pk)
            self.assertEqual(service.name, str(service_db))

    def test_is_object_is_instance(self):
        for service in self.service_set:
            self.assertTrue((isinstance(service, Service)))

    def test_filter(self):
        for service in self.service_set:
            service_db = Service.objects.filter(name=service.name).first()
            self.assertEqual(service, service_db)

    def test_update(self):
        for index, service in enumerate(self.service_set):
            service.name = f'TEST{index}'
            service.save()

            service_db = Service.objects.get(pk=service.pk)
            self.assertEqual(service, service_db)

    def test_model_integrity(self):
        with self.assertRaises(IntegrityError):
            service = Service()
            service.save()

    def test_get_images_method(self):
        for service in self.service_set:
            service_images = service.get_images()

            if service_images.exists():
                service_images = service_images.first()
                self.assertTrue(isinstance(service_images, ServiceImages))
            else:
                print('There is no images for this article.')


class TestServiceReservationModel(TestCase):
    def setUp(self) -> None:
        self.service_set = ServiceFactory.create_batch(5)
        self.user_set = UserFactory.create_batch(5)
        self.reservation_set = [
            ReservationFactory(user=user, service=service)
            for user, service in zip(self.user_set, self.service_set)
        ]

    def test_is_object_is_instance(self):
        for reservation in self.reservation_set:
            self.assertTrue(isinstance(reservation, ServiceReservation))

    def test_get(self):
        for reservation in self.reservation_set:
            service_reservation_db = ServiceReservation.objects.get(pk=reservation.pk)
            self.assertEqual(reservation, service_reservation_db)

    def test_filter(self):
        for reservation in self.reservation_set:
            service_reservation_db = ServiceReservation.objects.filter(date_time=reservation.date_time).first()
            self.assertEqual(reservation, service_reservation_db)

    def test_models_relation(self):
        for reservation in self.reservation_set:
            user_db = User.objects.get(pk=reservation.user.pk)
            service_db = Service.objects.get(pk=reservation.service.pk)

            self.assertEqual(reservation.user, user_db)
            self.assertEqual(reservation.service, service_db)

    def test_one_user_many_reservations(self):
        user = UserFactory(username='john_doe')
        reservation_set = [ReservationFactory(user=user) for _ in range(4)]

        user_reservations = ServiceReservation.objects.filter(user=user)
        self.assertEqual(user_reservations.count(), 4)

    def test_one_service_many_reservation(self):
        service = ServiceFactory(name='service1')
        reservation_set = [ReservationFactory(service=service) for _ in range(4)]

        service_reservations = ServiceReservation.objects.filter(service=service)
        self.assertEqual(service_reservations.count(), 4)

    def test_cascade_delete(self):
        for service in self.service_set:
            service.delete()
            self.assertFalse(ServiceReservation.objects.filter(service=service).exists())

        for user in self.user_set:
            user.delete()
            self.assertFalse(ServiceReservation.objects.filter(user=user).exists())

    def test_reservation_model_validation(self):
        with self.assertRaises(ValidationError):
            reservation = ReservationFactory(date_time='duppa')
            reservation. save()
