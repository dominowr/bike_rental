from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from rental.forms import MotorcycleReservationForm
from rental.views.utils import get_unavailable_dates, recently_viewed
from rental.models import Motorcycle


class BikeDetailView(FormMixin, DetailView):
    http_method_names = ['get']
    model = Motorcycle
    template_name = 'bike_detail/bike_detail.html'
    context_object_name = 'motorcycle'
    form_class = MotorcycleReservationForm

    def __init__(self):
        super().__init__()
        self.motorcycle = None

    def get_object(self, queryset=None):
        motorcycle_slug = self.kwargs.get('slug')
        motorcycle = get_object_or_404(self.model, slug=motorcycle_slug)

        self.motorcycle = motorcycle

        return motorcycle

    def get_context_data(self, **kwargs, ):
        context = super().get_context_data(**kwargs)
        unavailable_dates = get_unavailable_dates(motorcycle=self.motorcycle)
        price = float(self.motorcycle.rental_price)

        recently_viewed(self.request, self.motorcycle.id)

        recently_viewed_qs = self.model.objects.filter(pk__in=self.request.session.get('recently_viewed', []))

        if self.motorcycle.id in self.request.session.get('recently_viewed', []):
            recently_viewed_qs = recently_viewed_qs.exclude(id=self.motorcycle.id)

        recently_viewed_qs = sorted(recently_viewed_qs,
                                    key=lambda x: self.request.session['recently_viewed'].index(x.id))

        con = {
            'recently_viewed': recently_viewed_qs,
            'unavailable_dates': unavailable_dates,
            'rental_price_4_7_days': (price * 0.95),
            'rental_price_over_7_days': (price * 0.9),
        }

        for c in con:
            context[c] = con[c]

        return context
