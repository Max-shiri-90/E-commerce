from django.db import models

from accounts.models import User, Address
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='order')
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='items')
    size = models.CharField(max_length=12)
    color = models.CharField(max_length=12)
    quantity = models.SmallIntegerField()
    price = models.PositiveIntegerField()
    discount_price = models.FloatField(null=True, blank=True)


class AddressItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='address_item')
    address = models.ForeignKey(Address, on_delete=models.CASCADE,
                                related_name='address_item')


class DiscountCode(models.Model):
    name = models.CharField(max_length=10, unique=True)
    discount = models.SmallIntegerField(default=0)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.name
