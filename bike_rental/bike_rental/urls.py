import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('index.urls')),
    path('auth/', include('authentication.urls')),
    path('account/', include('user_account.urls')),
    path('rental/', include('rental.urls')),
    path('workshop/', include('workshop.urls')),
    path('contact/', include('contact.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.index_title = 'Administration'
admin.site.site_header = 'DnD Motorcycles administration'
admin.site.site_title = 'DnD Motorcycles'
