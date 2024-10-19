from django.contrib import admin

from .models import OrderItem, AddressItem, Order, DiscountCode


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem

    fieldsets = (
        ('order items', {'fields': ('product', 'size', 'color', 'quantity',
                                    'price', )}),)


class AddressItemAdmin(admin.TabularInline):
    model = AddressItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdmin, AddressItemAdmin, )
    search_fields = ('id', 'user',)
    list_display = ('id', 'user', 'total_price', 'is_paid', 'is_shipped',)
    list_filter = ('is_paid', 'is_shipped',)

    fieldsets = (('header', {'fields': ('user', 'total_price', 'is_paid',
                                        'is_shipped', )}),)


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'quantity')
