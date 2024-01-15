import factory
import factory.fuzzy
from authentication.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda u: 'user%d' % u)
    password = 'test'

    class Meta:
        model = User
