from django.contrib import admin
from .models import Motorcycle, MotorcycleReservation


class MotorcycleReservationAdmin(admin.ModelAdmin):
    list_display = ('motorcycle', 'start_date', 'end_date')


admin.site.register(Motorcycle)
admin.site.register(MotorcycleReservation, MotorcycleReservationAdmin)
