from django.test import TestCase
from django.db.utils import IntegrityError
from .news_factory import NewsFactory, NewsImagesFactory, UserFactory
from index.models import News, NewsImages
from authentication.models import User


class TestNewsModel(TestCase):
    def setUp(self) -> None:
        self.news_set = NewsFactory.create_batch(6)
        self.news_images_set = [NewsImagesFactory(news=news) for news in self.news_set]

    def test_get_and_str_method(self):
        for news in self.news_set:
            news_db = News.objects.get(pk=news.pk)
            self.assertEqual(news.title, str(news_db))

    def test_is_object_is_instance(self):
        for news in self.news_set:
            self.assertTrue(isinstance(news, News))

    def test_filter(self):
        for news in self.news_set:
            news_db = News.objects.filter(title=news.title).first()
            self.assertEqual(news, news_db)

    def test_update(self):
        for index, news in enumerate(self.news_set):
            news.title = f'TEST{index}'
            news.save()

            news_db = News.objects.get(pk=news.pk)
            self.assertEqual(news, news_db)

    def test_get_images_method(self):
        for news in self.news_set:
            news_images = news.get_images()

            if news_images.exists():
                news_image = news_images.first()
                self.assertTrue(isinstance(news_image, NewsImages))
            else:
                print('There is no images for this article.')

    def test_models_relation(self):
        for news in self.news_set:
            user_db = User.objects.get(pk=news.user.pk)

            self.assertEqual(news.user, user_db)

    def test_one_user_many_news(self):
        user = UserFactory()
        news_set = [NewsFactory(user=user) for _ in range(4)]
        self.assertEqual(len(news_set), 4)

    def test_news_model_integrity(self):
        with self.assertRaises(IntegrityError):
            news = News()
            news.save()


class TestNewsImagesModel(TestCase):
    def setUp(self) -> None:
        self.news_set = NewsFactory.create_batch(6)
        self.news_images_set = [NewsImagesFactory(news=news) for news in self.news_set]

    def test_models_relation(self):
        for news_image in self.news_images_set:
            news_db = News.objects.get(pk=news_image.news.pk)
            self.assertEqual(news_image.news, news_db)

    def test_cascade_delete(self):
        for news in self.news_set:
            news.delete()
            self.assertFalse(NewsImages.objects.filter(news=news).exists())

    def test_news_images_model_validation(self):
        with self.assertRaises(IntegrityError):
            news_images = NewsImages()
            news_images.save()
