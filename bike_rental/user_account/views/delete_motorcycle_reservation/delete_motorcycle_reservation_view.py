from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from rental.models import MotorcycleReservation


class DeleteMotorcycleReservation(DeleteView):
    http_method_names = ['post', 'get']
    model = MotorcycleReservation
    success_url = reverse_lazy('user_account:index-account')
    template_name = 'confirm_delete/confirm_delete_motorcycle_reservation.html'

    def post(self, request, *args, **kwargs):
        motorcycle_reservation_id = self.kwargs.get('pk')

        reservation = self.model.objects.filter(id=motorcycle_reservation_id, user=self.request.user).first()

        if reservation:
            send_mail(
                subject='Reservation was cancelled.',
                message=f'''
                Reservation for {reservation.motorcycle} from {reservation.start_date} to {reservation.end_date} was 
                cancelled.''',
                from_email=settings.EMAIL,
                recipient_list=[settings.EMAIL],
                fail_silently=False,
            )
            reservation.delete()

        return redirect(self.success_url)
