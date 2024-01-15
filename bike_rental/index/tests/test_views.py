from django.test import TestCase, Client
from django.shortcuts import reverse
from .news_factory import NewsFactory
from ..models import News


class TestIndexView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.index_url = reverse('index:index')
        self.news_set = NewsFactory.create_batch(6)

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_content(self):
        response = self.client.get(self.index_url)
        self.assertTrue('news' in response.context)

    def test_index_ordering(self):
        response = self.client.get(self.index_url)

