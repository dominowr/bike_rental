from django.views.generic import ListView
from index.models import News


class IndexView(ListView):
    model = News
    template_name = 'index.html'
    context_object_name = 'news'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-pub_date')[:4]

        return qs
