from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    slug = models.SlugField(blank=False)

    def __str__(self):
        return self.name

    def get_images(self):
        from . import ServiceImages
        return ServiceImages.objects.filter(service=self)
