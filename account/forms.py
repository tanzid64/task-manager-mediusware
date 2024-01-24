from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .constant import GENDER_TYPE

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'gender', 'password1', 'password2']