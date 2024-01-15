from django.test import TestCase
from django.db import IntegrityError
from .rental_factory import MotorcycleFactory, UserFactory, ReservationFactory
from rental.models import Motorcycle, MotorcycleReservation

from authentication.models import User


class TestMotorcycleModel(TestCase):
    def setUp(self) -> None:
        self.motorcycle_set = MotorcycleFactory.create_batch(5)

    def test_get_and_str_method(self):
        for motorcycle in self.motorcycle_set:
            motorcycle_db = Motorcycle.objects.get(pk=motorcycle.pk)
            self.assertEqual(motorcycle.model, str(motorcycle_db))

    def test_is_object_is_instance(self):
        for motorcycle in self.motorcycle_set:
            self.assertTrue(isinstance(motorcycle, Motorcycle))

    def test_filter(self):
        for motorcycle in self.motorcycle_set:
            motorcycle_db = Motorcycle.objects.filter(category=motorcycle.category).first()
            self.assertIn(motorcycle_db, self.motorcycle_set)

    def test_update(self):
        for index, motorcycle in enumerate(self.motorcycle_set):
            motorcycle.model = f'TEST{index}'
            motorcycle.save()

            motorcycle_db = Motorcycle.objects.get(pk=motorcycle.pk)
            self.assertEqual(motorcycle, motorcycle_db)

    def test_model_integrity(self):
        with self.assertRaises(IntegrityError):
            motorcycle = Motorcycle()
            motorcycle.save()


class TestMotorcycleReservationModel(TestCase):
    def setUp(self) -> None:
        self.motorcycle_set = MotorcycleFactory.create_batch(5)
        self.user_set = UserFactory.create_batch(5)
        self.reservation_set = [
            ReservationFactory(user=user, motorcycle=motorcycle)
            for user, motorcycle in zip(self.user_set, self.motorcycle_set)
        ]

    def test_is_object_is_instance(self):
        for reservation in self.reservation_set:
            self.assertTrue(isinstance(reservation, MotorcycleReservation))

    def test_get(self):
        for reservation in self.reservation_set:
            motorcycle_reservation_db = MotorcycleReservation.objects.get(pk=reservation.pk)
            self.assertEqual(reservation, motorcycle_reservation_db)

    def test_models_relation(self):
        for reservation in self.reservation_set:
            user_db = User.objects.get(pk=reservation.user.pk)
            motorcycle_db = Motorcycle.objects.get(pk=reservation.motorcycle.pk)
            self.assertEqual(reservation.motorcycle, motorcycle_db)
            self.assertEqual(reservation.user, user_db)

    def test_one_user_many_reservations(self):
        user = UserFactory()
        reservation_set = [ReservationFactory(user=user) for _ in range(4)]
        self.assertEqual(len(reservation_set), 4)

    def test_one_motorcycle_many_reservations(self):
        motorcycle = MotorcycleFactory()
        reservation_set = [ReservationFactory(motorcycle=motorcycle) for _ in range(4)]
        self.assertEqual(len(reservation_set), 4)

    def test_reservation_model_integrity(self):
        with self.assertRaises(IntegrityError):
            reservation = MotorcycleReservation()
            reservation.save()

