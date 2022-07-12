from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import index, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("accounts.urls")),
    path('product/', include("inventory.urls")),
    path('', home, name='home'),
    path('order/', include("orders.urls")),
    # path('home', home, name='home'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
