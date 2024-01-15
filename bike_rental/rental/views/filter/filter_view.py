from django.views.generic import ListView
from django.http import Http404
from rental.models import Motorcycle


class FilterView(ListView):
    http_method_names = ['get']
    model = Motorcycle
    template_name = 'index_rental/index_rental.html'
    context_object_name = 'motorcycles'

    def get_queryset(self):
        queryset = super().get_queryset()
        capacity_from = self.request.GET.get('capacity_from')
        capacity_to = self.request.GET.get('capacity_to')
        category_slug = self.kwargs.get('slug')

        if category_slug:
            category = category_slug.capitalize()
            queryset = queryset.filter(category=category)

            if not queryset:
                raise Http404

        if capacity_from:
            queryset = queryset.filter(capacity__gte=capacity_from)

        if capacity_to:
            queryset = queryset.filter(capacity__lte=capacity_to)

        queryset = queryset.order_by('id')

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')

        con = {
            'slug': slug,
            'capacity_from': self.request.GET.get('capacity_from', ''),
            'capacity_to': self.request.GET.get('capacity_to', ''),
            'categories': Motorcycle.objects.values('category').distinct()
        }

        for c in con:
            context[c] = con[c]

        return context
