from django.contrib import admin
from .models import Service, ServiceReservation, ServiceImages


class ServiceImagesInline(admin.StackedInline):
    model = ServiceImages


class ServiceAdmin(admin.ModelAdmin):
    inlines = [
        ServiceImagesInline
    ]


class ServiceReservationAdmin(admin.ModelAdmin):
    list_display = ('service', 'get_date', 'get_time')

    def get_date(self, obj):
        return obj.date_time.date()
    get_date.short_description = 'Date'

    def get_time(self, obj):
        return obj.date_time.time()
    get_time.short_description = 'Time'


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceReservation, ServiceReservationAdmin)
