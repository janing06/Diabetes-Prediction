from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('diabetes.urls')),
    path('favicon.ico', lambda _ : redirect('static/img/brand/dark.svg', permanent=True)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Naval Diabetes' 
admin.site.index_title = 'Dashboard'                 
admin.site.site_title = 'Admin' 