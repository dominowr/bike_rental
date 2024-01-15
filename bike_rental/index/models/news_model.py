from django.db import models
from authentication.models import User


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    summary = models.TextField(max_length=250)
    text = models.TextField()
    pub_date = models.DateTimeField()
    slug = models.SlugField(blank=False)

    def __str__(self):
        return self.title

    def get_images(self):
        from . import NewsImages
        return NewsImages.objects.filter(news=self)
