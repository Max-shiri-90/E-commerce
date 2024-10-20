from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import PermissionDenied


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given phone, and password.
        """
        if not phone:
            raise ValueError('Users must have an phone address')

        user = self.model(
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given phone, and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True,
                              unique=True)
    fullname = models.CharField(max_length=50,  null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='addresses')
    fullname = models.CharField(max_length=40)
    phone = models.CharField(max_length=12)
    address_provience = models.CharField(max_length=50)
    address_city = models.CharField(max_length=50)
    address_street = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        address = self.address_provience + " - " + self.address_city + " - " \
            + self.address_street + " - " + self.postal_code + " - " + \
            self.fullname + " - " + self.phone
        return address

    def save(self):
        address = Address.objects.filter(user=self.user)
        if address.count() > 2:
            raise PermissionDenied
        else:
            super(Address, self).save()
