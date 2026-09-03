from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tenants.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('cohorts.urls')),
    path('api/', include('applications.urls')),
    path('api/', include('payments.urls')),
    path('api/', include('academics.urls')),
    path('api/', include('attendance.urls')),
    path('api/', include('certificates.urls')),
    path('api/', include('communications.urls')),
    path('api/', include('classwork.urls')),
    path('api/', include('exams.urls')),
    path('api/', include('results.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)