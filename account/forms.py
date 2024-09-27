from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core import validators

from .models import User, Address


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'email', 'password', 'is_active', 'is_admin')


class RegisterForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 11:
            raise ValidationError('phone number must have 11 characters',
                                  code='invalid phone')
        return phone


class CheckOtpForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'}),
        validators=[validators.MaxLengthValidator(5)])
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'}))


class AddressCreationForm(forms.ModelForm):
    user = forms.IntegerField(required=False)

    class Meta:
        model = Address
        fields = '__all__'


class ProfileForm(forms.ModelForm):
    """
    A form for updating profile. Includes fullname and email fields
    on the profile, but it has phone as a readonly field.
    """
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = ('phone', 'fullname', 'email')

    def clean_phone(self):
        return self.initial['phone']
