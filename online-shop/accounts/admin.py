from django.contrib import admin

from accounts.models import Customer, Supplier, CustomerWallet


admin.site.register(Customer)
admin.site.register(Supplier)
# admin.site.register(Address)
admin.site.register(CustomerWallet)
