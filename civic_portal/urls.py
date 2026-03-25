from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import RedirectView

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', RedirectView.as_view(url='/dashboard/admin/', permanent=False)),
    path('api/users/', include('users.urls')),
    path('api/', include('wards.urls')),
    path('api/', include('departments.urls')),
    path('api/', include('complaints.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('audit.urls')),
    path('', include('frontend.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
