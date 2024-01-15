from django.db import models


class Motorcycle(models.Model):
    model = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    year = models.IntegerField()
    engine = models.CharField(max_length=100)
    torque = models.IntegerField()
    capacity = models.IntegerField()
    top_speed = models.IntegerField()
    wet_weight = models.IntegerField()
    fuel_capacity = models.IntegerField()
    image = models.ImageField(upload_to='images/rental')
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(blank=False)

    def __str__(self):
        return self.model
