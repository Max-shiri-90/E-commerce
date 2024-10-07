from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from lakers import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("product.urls")),
    path('account/', include("account.urls")),
    path('cart/', include("order.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
