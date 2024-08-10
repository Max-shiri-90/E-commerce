from random import randint
from uuid import uuid4

from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth import login, logout as logout_

from .forms import RegisterForm, CheckOtpForm, AddressCreationForm, ProfileForm
from .models import Otp, User, Address

import ghasedakpack


SMS = ghasedakpack.Ghasedak(
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")


class RegisterView(View):
    """
    Register with phone-number and otp-code registeration
    """
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(10000, 99999)
            SMS.verification({'receptor': cd["phone"], 'type': '1',
                              'template': 'randcode', 'param1': randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            return redirect(reverse('account:check-otp')+f'?token={token}')
        else:
            form.add_error('phone', 'invalid data')
        return render(request, 'account/register.html', {'form': form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'account/check-otp.html', {'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_create = User.objects.get_or_create(phone=otp.phone)
                login(request, user)
                return redirect('/')
        else:
            form.add_error('phone', 'invalid data')
        return render(request, 'account/check-otp.html', {'form': form})


class AddAddressView(View):
    def get(self, request):
        form = AddressCreationForm(request.GET)
        return render(request, 'account/add-address.html', {'form': form})

    def post(self, request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
        return render(request, 'account/add-address.html', {'form': form})


class DeleteAddressView(DeleteView):
    model = Address
    template_name = 'account/delete-address.html'
    success_url = reverse_lazy('account:add-address')


class ProfileView(UpdateView):
    model = User
    template_name = 'account/profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('account:profile', kwargs={'pk': self.object.pk})


def logout(request):
    logout_(request)
    return redirect('/')
