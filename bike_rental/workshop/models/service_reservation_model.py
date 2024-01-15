from django.db import models
from core.base_model import BaseModel
from authentication.models import User
from . import Service


class ServiceReservation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
