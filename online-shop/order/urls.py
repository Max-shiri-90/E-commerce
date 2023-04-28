from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path('detail/', views.CartDetailView.as_view(), name='cart-detail'),
    path('add/<int:pk>', views.CartAddView.as_view(), name='cart-add'),
    path('delete/<str:id>', views.CartDeleteView.as_view(), name='cart-delete'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('order/add/', views.OrderAddView.as_view(), name='order-add'),
    path('applydiscount/<int:pk>', views.ApplyDiscountView.as_view(), name='apply-discount'),
]