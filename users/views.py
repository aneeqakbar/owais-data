from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin


class SettingsView(View):
    def get(self, request):
        return render(request, 'auth/settings.html')

class Settings1View(View):
    def get(self, request):
        return render(request, 'auth/settings1.html')


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'auth/signup.html', {'form': form})

    def  post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('users:login')
        return render(request, 'auth/register.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request, 'auth/profile.html', context)

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users:ProfileView')
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'auth/profile.html', context)
