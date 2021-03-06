from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, phone="", **extra_fields):

        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, phone="",  **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, phone, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, validators=[RegexValidator(r'^09\d{9}$')], unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_user'


class Address(User):
    province = models.CharField('استان', max_length=255)
    city = models.CharField('شهر', max_length=255)
    customer_address = models.ForeignKey('Customer', on_delete=models.CASCADE)
    supplier_address = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = 'Address'

    def __str__(self):
        return f"{self.city}"


class Customer(User):
    bank_info = models.CharField(max_length=250, null=True, blank=True)
    joined_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Customer'

    def __str__(self):
        return self.email


class Supplier(User):
    bank_info = models.CharField(max_length=250, null=True, blank=True)
    company_name = models.CharField(max_length=100)
    joined_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Supplier'

    def __str__(self):
        return self.company_name


class CustomerWallet(models.Model):
    bank_info = models.CharField(max_length=250)
    credit = models.CharField(max_length=250)
    payment_info = models.JSONField({})
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

