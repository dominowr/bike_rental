from django.db import models
from core.base_model import BaseModel
from authentication.models import User
from . import Motorcycle


class MotorcycleReservation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ['start_date', 'end_date', 'is_deleted']
