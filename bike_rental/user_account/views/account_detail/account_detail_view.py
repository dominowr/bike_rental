from django.views.generic import TemplateView
from user_account.views.utils import get_unavailable_dates_dict, get_unavailable_hours_dict


class UserAccountView(TemplateView):
    template_name = 'account_detail/account_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        motorcycle_reservations = sorted(
            user.motorcyclereservation_set.all(), key=lambda x: x.id
        )
        service_reservations = sorted(
            user.servicereservation_set.all(), key=lambda x: x.id
        )

        unavailable_dates_dict = get_unavailable_dates_dict(motorcycle_reservations)
        unavailable_dates_hours_dict = get_unavailable_hours_dict(service_reservations)

        con = {
            'service_reservations': service_reservations,
            'motorcycle_reservations': motorcycle_reservations,
            'unavailable_dates': unavailable_dates_dict,
            'unavailable_hours': unavailable_dates_hours_dict,
            'user': user,
        }

        context.update(con)

        return context



