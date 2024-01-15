import factory
import datetime
import factory.fuzzy
from pytz import UTC
from workshop.models import Service, ServiceReservation, ServiceImages
from authentication.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda u: 'user%d' % u)
    password = 'test'

    class Meta:
        model = User


class ServiceFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'name%d' % n)
    description = 'test'
    price = factory.fuzzy.FuzzyInteger(50, 2000)
    slug = factory.LazyAttribute(lambda obj: 'slug%s' % obj.name)

    class Meta:
        model = Service


class ServiceImagesFactory(factory.django.DjangoModelFactory):
    service = factory.SubFactory(ServiceFactory)
    image = factory.Sequence(lambda i: 'images/workshop/image%d' % i)

    class Meta:
        model = ServiceImages


class ReservationFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    service = factory.SubFactory(ServiceFactory)
    date_time = factory.fuzzy.FuzzyDateTime(datetime.datetime(2022, 10, 1, tzinfo=UTC))

    class Meta:
        model = ServiceReservation
