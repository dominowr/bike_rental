from django.contrib import admin
from .models import News, NewsImages


class NewsImagesInline(admin.StackedInline):
    model = NewsImages


class NewsAdmin(admin.ModelAdmin):
    inlines = [
        NewsImagesInline
    ]


admin.site.register(News, NewsAdmin)
