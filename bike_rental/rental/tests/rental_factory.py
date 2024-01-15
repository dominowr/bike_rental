import factory
import datetime
import factory.fuzzy
from rental.models import Motorcycle, MotorcycleReservation
from authentication.models import User


class MotorcycleFactory(factory.django.DjangoModelFactory):
    model = factory.Sequence(lambda n: 'motorcycle%d' % n)
    category = factory.fuzzy.FuzzyChoice(['sport', 'enduro', 'cruiser', 'touring'])
    description = 'test'
    engine = 'test'
    torque = 0
    capacity = 0
    top_speed = 0
    wet_weight = 0
    fuel_capacity = 0
    year = factory.fuzzy.FuzzyInteger(1980, 2000)
    image = factory.Sequence(lambda i: 'images/rental/image%d' % i)
    rental_price = 0
    slug = factory.LazyAttribute(lambda obj: 'slug-%s' % obj.model)

    class Meta:
        model = Motorcycle


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda u: 'user%d' % u)
    password = 'test'

    class Meta:
        model = User


class ReservationFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    motorcycle = factory.SubFactory(MotorcycleFactory)
    start_date = factory.Faker(
        'date_between',
        start_date='-30d',
        end_date='-15d'
    )
    end_date = factory.Faker(
        'date_between',
        start_date='-15d',
        end_date=datetime.date.today()
    )

    class Meta:
        model = MotorcycleReservation
