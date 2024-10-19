from django.contrib import admin

from . import models


class InformationAdmin(admin.StackedInline):
    model = models.Information

    verbose_name = 'Information'
    verbose_name_plural = 'Information'


class ImageAdmin(admin.StackedInline):
    model = models.ProductImage


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title',)
    list_display = ('id', 'title', 'price', 'quantity',)
    inlines = (ImageAdmin, InformationAdmin, )

    fieldsets = (
        ('header', {'fields': ('title', 'price', 'discount_price',
                               'discount_percentage', 'quantity',
                               'description', 'category', 'size', 'color',)}),
    )


admin.site.register(models.Category)
admin.site.register(models.Color)
admin.site.register(models.Size)
admin.site.register(models.Like)
