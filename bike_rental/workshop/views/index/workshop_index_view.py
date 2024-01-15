from django.views.generic import ListView
from workshop.models import Service


class WorkshopIndexView(ListView):
    http_method_names = ['get']
    model = Service
    template_name = 'index_workshop/index_workshop.html'
    context_object_name = 'services'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')

        return queryset
