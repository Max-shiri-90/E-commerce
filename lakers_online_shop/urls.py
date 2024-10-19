from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from lakers_online_shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("products.urls")),
    path('accounts/', include("accounts.urls")),
    path('cart/', include("orders.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)