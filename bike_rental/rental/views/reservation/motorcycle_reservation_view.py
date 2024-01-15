import pandas as pd
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView
from django.contrib import messages
from rental.views.utils import get_unavailable_dates, send_confirmation_mail
from rental.models import Motorcycle, MotorcycleReservation
from rental.forms import MotorcycleReservationForm


class CreateMotorcycleReservation(CreateView):
    http_method_names = ['post']
    model = MotorcycleReservation
    form_class = MotorcycleReservationForm

    def form_invalid(self, form):
        motorcycle_slug = self.request.GET.get('slug')
        for error in form.non_field_errors():
            messages.error(self.request, error)
        return redirect('rental:bike-detail', slug=motorcycle_slug)

    def form_valid(self, form):
        user = self.request.user
        motorcycle_slug = self.request.GET.get('slug')

        if not user.is_authenticated:
            messages.error(self.request, 'Only login user can reserve motorcycle.')
            return redirect('rental:bike-detail', slug=motorcycle_slug)

        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        date_range = pd.date_range(start_date, end_date).strftime('%Y-%m-%d')

        motorcycle = get_object_or_404(Motorcycle, slug=motorcycle_slug)
        unavailable_dates = get_unavailable_dates(motorcycle)

        if any(date in unavailable_dates for date in date_range):
            messages.error(self.request, 'Sorry this date is unavailable.')
            return redirect('rental:bike-detail', slug=motorcycle_slug)

        reservation = MotorcycleReservation(
            user=user,
            motorcycle=motorcycle,
            start_date=start_date,
            end_date=end_date,
        )

        reservation.save()

        send_confirmation_mail(user, motorcycle, start_date, end_date, date_range)

        messages.success(self.request, 'Your reservation was created. You will receive e-mail with details.')

        return redirect('rental:bike-detail', slug=motorcycle_slug)
