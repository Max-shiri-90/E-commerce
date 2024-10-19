from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .cart_module import Cart
from .models import Order, OrderItem, DiscountCode
from products.models import Product


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "orders/cart.html", {'cart': cart})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        size, color, quantity, price, discount_price = request.POST.get(
            'size', '-'), request.POST.get('color', '-'), request.POST.get(
            'quantity'), request.POST.get('price'), request.POST.get(
            'discount_price')
        cart = Cart(request)
        cart.add(product, size, color, quantity, price, discount_price)
        return redirect('orders:cart-detail')


class CartDeleteView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('orders:cart-detail')


class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, 'orders/order-detail.html', {'order': order})


class OrderAddView(View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user,
                                     total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'],
                                     size=item['size'], color=item['color'],
                                     quantity=item['quantity'],
                                     price=item['price'])
        return redirect('orders:order-detail', order.id)


class ApplyDiscountView(View):
    def post(self, request, pk):
        code = request.POST.get('discount_code')
        order = get_object_or_404(Order, id=pk)
        discount_code = get_object_or_404(DiscountCode, name=code)
        if discount_code.quantity == 0:
            return redirect('orders:order-detail', order.id)
        order.total_price -= order.total_price*discount_code.discount/100
        order.save()
        discount_code.quantity -= 1
        discount_code.save()
        return redirect('orders:order-detail', order.id)
