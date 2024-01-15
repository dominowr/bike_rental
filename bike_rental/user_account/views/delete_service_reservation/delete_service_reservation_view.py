from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from workshop.models import ServiceReservation


class DeleteServiceReservation(DeleteView):
    http_method_names = ['post', 'get']
    model = ServiceReservation
    success_url = reverse_lazy('user_account:index-account')
    template_name = 'confirm_delete/confirm_delete_service_reservation.html'

    def post(self, request, *args, **kwargs):
        service_reservation_id = self.kwargs.get('pk')

        reservation = self.model.objects.filter(id=service_reservation_id, user=self.request.user).first()

        if reservation:
            send_mail(
                subject='Reservation was cancelled.',
                message=f'''
                Reservation for {reservation.service.name} from {reservation.date_time} was 
                cancelled.''',
                from_email=settings.EMAIL,
                recipient_list=[settings.EMAIL],
                fail_silently=False,
            )
            reservation.delete()

        messages.success(request, 'Your reservation has been deleted successfully.')

        return redirect(self.success_url)
