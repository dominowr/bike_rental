import factory
import random
from django.utils import timezone
from index.models import News, NewsImages
from authentication.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda u: 'user%d' % u)
    password = 'test'

    class Meta:
        model = User


class NewsFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: 'news%d' % n)
    summary = 'test'
    text = 'test'
    pub_date = factory.LazyFunction(
        lambda: timezone.now() - timezone.timedelta(days=random.randint(1, 10))
    )
    slug = factory.LazyAttribute(lambda obj: 'slug%s' % obj.title)

    class Meta:
        model = News


class NewsImagesFactory(factory.django.DjangoModelFactory):
    news = factory.SubFactory(NewsFactory)
    image = factory.Sequence(lambda i: 'images/news/image%d' % i)

    class Meta:
        model = NewsImages
