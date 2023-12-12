from django import forms

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User

class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'id_card', 'auth', 'degree', 'password1', 'password2']
