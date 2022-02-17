from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings

handler404 = 'accruals.errors.page_not_found'
handler500 = 'accruals.errors.server_error'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('', include('accruals.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
