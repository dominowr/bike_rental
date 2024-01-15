from datetime import datetime
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView
from django.contrib import messages
from workshop.views.utils import get_unavailable_hours, send_confirmation_mail
from workshop.models import ServiceReservation, Service
from workshop.forms import ServiceReservationForm


class CreateWorkshopReservation(CreateView):
    http_method_names = ['post']
    model = ServiceReservation
    form_class = ServiceReservationForm

    def form_invalid(self, form):
        service_slug = self.request.GET.get('slug')
        for error in form.non_field_errors():
            messages.error(self.request, error)
        return redirect('workshop:service-workshop', slug=service_slug)

    def form_valid(self, form):
        user = self.request.user
        service_slug = self.request.GET.get('slug')

        if not user.is_authenticated:
            messages.error(self.request, 'Only login user can reserve service meeting.')
            return redirect('workshop:service-workshop', slug=service_slug)

        service = get_object_or_404(Service, slug=service_slug)
        unavailable_hours = get_unavailable_hours(service_slug)
        selected_date = datetime.strftime(form.cleaned_data['date'], '%Y-%m-%d')
        selected_hour = form.cleaned_data['hour']
        date_time = form.cleaned_data['date_time']

        if selected_date in unavailable_hours and selected_hour in unavailable_hours[selected_date]:
            messages.error(self.request, 'Sorry, this date is unavailable.')
            return redirect('workshop:service-workshop', slug=service_slug)

        appointment = self.model(
            user=user,
            service=service,
            date_time=date_time
        )

        appointment.save()

        send_confirmation_mail(user, service, selected_date, selected_hour)

        messages.success(self.request, 'Your appointment was set correctly. You will receive e-mail with details.')

        return redirect('workshop:service-workshop', slug=service_slug)

