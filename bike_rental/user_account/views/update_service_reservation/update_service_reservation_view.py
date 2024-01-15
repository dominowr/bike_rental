from datetime import datetime, time
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from workshop.models import ServiceReservation
from user_account.views.utils import get_unavailable_hours_dict


class UpdateServiceReservationView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        date_str = self.request.POST.get('date')
        hour_str = self.request.POST.get('hour')

        reservation_as_list = [get_object_or_404(ServiceReservation, pk=self.kwargs.get('pk'))]

        reservation = reservation_as_list[0]
        service = reservation.service

        current_date = datetime.now().date()
        open_hour = time(7, 0)
        close_hour = time(16, 0)

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            hour = datetime.strptime(hour_str, '%I:%M %p').time()

            if date >= current_date and open_hour <= hour <= close_hour:
                date_time = timezone.make_aware(datetime.combine(
                    date, hour
                ))
            else:
                raise ValueError

        except ValueError:
            messages.error(request, 'Invalid date or time format.')
            return redirect('user_account:index-account')

        unavailable_hours = get_unavailable_hours_dict(reservation_as_list)

        if date in unavailable_hours[service] and hour in unavailable_hours[service][date]:
            messages.error(request, 'Sorry, this date is unavailable.')
            return redirect('user_account:index-account')

        previous_date = reservation.date_time

        reservation.date_time = date_time
        reservation.save()

        user = request.user

        send_mail(
            subject='Reservation was updated',
            message=f'''
            Reservation for {reservation.service.name} was moved from {previous_date} to {reservation.date_time}
            ''',
            from_email=settings.EMAIL,
            recipient_list=[settings.EMAIL, user.email],
            fail_silently=False,
        )

        messages.success(
            request, 'Your reservation has been updated successfully. You will receive email with info.'
        )

        return redirect('user_account:index-account')

