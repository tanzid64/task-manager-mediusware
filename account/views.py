from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import User
from .forms import UserRegistrationForm
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from task.models import Task
# Create your views here.
class UserRegistrationView(CreateView):
    template_name = 'account/account.html'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('homepage')
    def form_valid(self, form):
        messages.success(self.request, 'User creation successfull, please check your email to active account.')
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Registration'
        return context

class UserLoginView(LoginView):
    template_name = 'account/account.html'
    def get_success_url(self):
        return reverse_lazy('homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'LogIn'
        return context
    
def UserLogoutView(request):
    logout(request)
    return redirect('login')

class UserProfileView(DetailView):
    template_name = 'account/profile.html'
    model = User
    def get_object(self):
        return self.request.user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Edit Profile'
        context['task_history'] = Task.objects.filter(completed_by=self.request.user)
        return context
    
class UserProfileUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'account/account.html'
    model = User
    fields= ['username', 'email', 'phone', 'gender']
    success_url = reverse_lazy('profile')
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.danger(self.request, 'Information Incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Edit Profile'
        return context
    
class UserPasswordUpdateView(LoginRequiredMixin,PasswordChangeView):
    template_name = 'account/account.html'
    success_url = reverse_lazy('profile')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Edit Password'
        return context