from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import User
from .forms import UserRegistrationForm, UserProfileUpdateForm, LoginForm
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from task.models import Task
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
# Create your views here.
class UserRegistrationView(CreateView):
    template_name = 'account/registration.html'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('homepage')
    def form_valid(self, form):
        messages.success(self.request, 'User creation successfull, please check your email to active account.')
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = LoginForm
    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Sign in successfull.')
        return super().form_valid(form)
    
    
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
        context['task_history'] = Task.objects.filter(completed_by=self.request.user).count()
        return context
    
class UserProfileUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'account/profile_update.html'
    model = User
    form_class = UserProfileUpdateForm
    # fields= ['username','first_name','last_name', 'email', 'phone', 'gender']
    success_url = reverse_lazy('profile')
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Information Incorrect')
        return super().form_invalid(form)
    
class UserPasswordUpdateView(LoginRequiredMixin,PasswordChangeView):
    template_name = 'account/pass_change.html'
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, "Password Updated Successfully.")
        return super().form_valid(form)