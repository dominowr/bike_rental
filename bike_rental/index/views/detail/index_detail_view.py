from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from ...models import News


class IndexDetailView(DetailView):
    model = News
    template_name = 'detail/index_detail.html'
    context_object_name = 'news'

    def get_object(self, queryset=None):
        news_slug = self.kwargs.get('slug')
        news = get_object_or_404(self.model, slug=news_slug)

        return news
