from django.db import models
from . import Service


class ServiceImages(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/workshop')
