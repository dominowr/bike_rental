import pandas as pd
from datetime import datetime
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from rental.models import MotorcycleReservation
from user_account.views.utils import get_unavailable_dates_dict


class UpdateMotorcycleReservationView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        start_date_str = self.request.POST.get('start-date')
        end_date_str = self.request.POST.get('end-date')

        reservation_as_list = [get_object_or_404(MotorcycleReservation, pk=self.kwargs.get('pk'))]

        reservation = reservation_as_list[0]
        motorcycle = reservation.motorcycle

        current_date = datetime.now().date()

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            if start_date >= current_date and end_date >= current_date and not end_date < start_date:
                date_range = pd.date_range(start_date_str, end_date_str).strftime('%Y-%m-%d')
            else:
                raise ValueError

        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('user_account:index-account')

        unavailable_dates = get_unavailable_dates_dict(reservation_as_list)

        if any(date in unavailable_dates[motorcycle] for date in date_range):
            messages.error(request, 'Sorry, this date is unavailable.')
            return redirect('user_account:index-account')

        reservation.start_date = start_date
        reservation.end_date = end_date
        reservation.save()

        user = request.user

        send_mail(
            subject='Reservation was updated',
            message=f'''
                Reservation for {reservation.motorcycle} was moved on:
                Start date: {reservation.start_date}
                End date: {reservation.end_date}
                ''',
            from_email=settings.EMAIL,
            recipient_list=[settings.EMAIL, user.email],
            fail_silently=False,
        )

        messages.success(
            request, 'Your reservation has been updated. You will receive an email with info.'
        )

        return redirect('user_account:index-account')




