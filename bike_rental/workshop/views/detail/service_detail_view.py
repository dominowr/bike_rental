from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from workshop.forms import ServiceReservationForm
from workshop.models import Service
from workshop.views.utils import get_unavailable_hours


class ServiceDetailView(FormMixin, DetailView):
    http_method_names = ['get']
    model = Service
    template_name = 'service_detail/service_detail.html'
    context_object_name = 'service'
    form_class = ServiceReservationForm

    def __init__(self):
        super().__init__()
        self.service = None

    def get_object(self, queryset=None):
        service_slug = self.kwargs.get('slug')
        service = get_object_or_404(self.model, slug=service_slug)

        self.service = service

        return service

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        unavailable_hours = get_unavailable_hours(self.service.slug)

        context['unavailable_hours'] = unavailable_hours
        return context
