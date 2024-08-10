from django.db import models
from django.utils.text import slugify

from account.models import User


class Size(models.Model):
    title = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Size'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=10)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=40)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(null=True, blank=True)

    price = models.IntegerField()
    discount_price = models.FloatField(null=True, blank=True)
    discount_percentage = models.FloatField(default=0)

    quantity = models.SmallIntegerField()
    description = models.TextField()
    added_date = models.DateField(auto_now_add=True)

    size = models.ManyToManyField(Size, blank=True, related_name="products")
    color = models.ManyToManyField(Color, blank=True, related_name="products")
    category = models.ManyToManyField(Category, blank=True,
                                      related_name="products")

    def __str__(self):
        return str(self.id)

    def delete(self):
        images = ProductImage.objects.filter(product=self)
        for image in images:
            image.delete()
        super(Product, self).delete()

    def get_absolute_url(self):
        return f"/product/{self.slug}/{self.pk}/"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.discount_percentage > 0:
            self.discount_price = self.price - (self.price *
                                                self.discount_percentage) / 100
        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to='products')

    def delete(self, *args, **kwargs):
        self.image.delete()
        return super(ProductImage, self).delete(*args, **kwargs)

    def remove_on_image_update(self):
        try:
            obj = ProductImage.objects.get(id=self.id)
        except ProductImage.DoesNotExist:
            return
        if obj.image and self.image and obj.image != self.image:
            obj.image.delete()

    def save(self, *args, **kwargs):
        self.remove_on_image_update()
        return super(ProductImage, self).save(*args, **kwargs)


class Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='informations')
    text = models.TextField()

    def __str__(self):
        return self.text[:30]


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='likes')

    def __str__(self):
        return f"{self.product.id} - {self.user.phone}"
