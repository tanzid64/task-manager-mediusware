from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .constant import GENDER_TYPE

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'gender', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For other all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
            'class': (
                'appearance-none block w-full bg-gray-200 '
                'text-gray-700 border border-gray-200 rounded '
                'py-3 px-4 leading-tight focus:outline-none '
                'focus:bg-white focus:border-gray-500'
            )
        })

class UserProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'phone', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For other all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
            'class': (
                'appearance-none block w-full bg-gray-200 '
                'text-gray-700 border border-gray-200 rounded '
                'py-3 px-4 leading-tight focus:outline-none '
                'focus:bg-white focus:border-gray-500'
            ),
            'required': False
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email address is already in use.')

        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This phone address is already in use.')

        return phone
    
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For other all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
            'class': (
                'appearance-none block w-full bg-gray-200 '
                'text-gray-700 border border-gray-200 rounded '
                'py-3 px-4 leading-tight focus:outline-none '
                'focus:bg-white focus:border-gray-500'
            )
        })