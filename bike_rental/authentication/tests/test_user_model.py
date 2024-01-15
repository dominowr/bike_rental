from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import IntegrityError
from authentication.models import User
from .user_factory import UserFactory


class TestUserModel(TestCase):
    def setUp(self) -> None:
        self.user_set = UserFactory.create_batch(5)

    def test_new_user_is_inactive(self):
        for user in self.user_set:
            user_db = User.objects.get(pk=user.pk)
            self.assertFalse(user_db.is_active)

    def test_str_method(self):
        for user in self.user_set:
            user_db = User.objects.get(pk=user.pk)
            self.assertEqual(user, user_db)

    def test_is_object_is_instance(self):
        for user in self.user_set:
            self.assertTrue(isinstance(user, User))

    def test_user_model_validation(self):
        user = UserFactory()
        user.save()
        self.assertRaises(IntegrityError)
