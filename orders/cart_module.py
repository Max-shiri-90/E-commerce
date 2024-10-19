from products.models import Product


CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            product = Product.objects.get(id=int(item['id']))
            item['product'] = Product.objects.get(id=int(item['id']))
            if item['discount_price']:
                item['total'] = int(item['quantity']) *\
                                int(item['discount_price'])
            else:
                item['total'] = int(item['quantity'])*int(item['price'])
            item['unique_id'] = self.unique_id_generator(
                product.id, item['size'], item['color'])
            yield item

    def unique_id_generator(self, id, size, color):
        result = f'{id}-{size}-{color}'
        return result

    def add(self, product, size, color, quantity, price, discount_price):
        unique = self.unique_id_generator(product.id, size, color)
        if unique not in self.cart:
            self.cart[unique] = {'id': str(product.id), 'size': size,
                                 'color': color, 'quantity': 0,
                                 'price': product.price,
                                 'discount_price': product.discount_price}
        self.cart[unique]['quantity'] += int(quantity)
        self.save()

    def sub_total(self):
        cart = self.cart.values()
        for item in cart:
            if item['discount_price']:
                item['total'] = int(item['quantity']) * int(
                                   item['discount_price'])
            else:
                item['total'] = int(item['quantity'])*int(item['price'])
        cart_sub_total = sum(int(item['total']) for item in cart)
        return cart_sub_total

    def total(self):
        cart_total = Cart.sub_total(self) + 10
        return cart_total

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def save(self):
        self.session.modified = True

    def remove_cart(self):
        del self.session[CART_SESSION_ID]
