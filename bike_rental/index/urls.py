from django.urls import path
from .views import IndexView, IndexDetailView


app_name = 'index'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('news/<slug:slug>/', IndexDetailView.as_view(), name='news-detail'),
]


