from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Otp, Address
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    search_fields = ('phone',)
    list_display = ('phone', 'is_admin', 'fullname')
    list_filter = ('is_admin',)
    fieldsets = (
        ('account', {'fields': ('phone',)}),
        ('personal information', {'fields': ('fullname', 'email', )}),
        ('access level', {'fields': ('is_admin', 'is_active', )}),
    )

    add_fieldsets = (
        ('add new user', {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'fullname', 'password1', 'password2')
            }),)

    ordering = ('phone',)
    filter_horizontal = ()


admin.site.register(Address)
admin.site.register(User, UserAdmin)
admin.site.register(Otp)
admin.site.unregister(Group)
