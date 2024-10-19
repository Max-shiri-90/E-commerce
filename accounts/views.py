from random import randint
from uuid import uuid4

from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth import login, logout as logout_
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import RegisterForm, CheckOtpForm, AddressCreationForm, ProfileForm
from .models import Otp, User, Address

import ghasedakpack


SMS = ghasedakpack.Ghasedak("YOUR_GHASEDAK_PACK_API_KEY")


class RegisterView(View):
    """
    Register with phone-number and otp-code registeration
    """
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            global randcode 
            randcode = randint(10000, 99999)
            print('enter this randcode to login: ', randcode)
            SMS.verification({'receptor': cd["phone"], 'type': '1',
                              'template': 'randcode', 'param1': randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            return redirect(reverse('accounts:check-otp')+f'?token={token}')
        else:
            form.add_error('phone', 'invalid data')
        return render(request, 'accounts/register.html', {'form': form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'accounts/check-otp.html', {
            'form': form, 
            'randcode': randcode
            })

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
            form.add_error('phone', 'invalid data...')
        return render(request, 'accounts/check-otp.html', {'form': form})


class AddAddressView(View):
    def get(self, request):
        form = AddressCreationForm(request.GET)
        return render(request, 'accounts/add-address.html', {'form': form})

    def post(self, request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
        return render(request, 'accounts/add-address.html', {'form': form})


class DeleteAddressView(DeleteView):
    model = Address
    template_name = 'accounts/delete-address.html'
    success_url = reverse_lazy('accounts:add-address')


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user


def logout(request):
    logout_(request)
    return redirect('/')
