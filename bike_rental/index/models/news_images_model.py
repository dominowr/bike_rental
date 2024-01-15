from django.db import models
from . import News


class NewsImages(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/news', null=True, blank=True)
