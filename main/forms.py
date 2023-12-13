from typing import Any
from django import forms

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Code, User

class SignUpForm(UserCreationForm):
    code = forms.CharField()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'code', 'id_card', 'auth', 'degree', 'password1', 'password2']

    def clean(self):
        codes = Code.objects.filter(phone_number=self.cleaned_data['phone_number'], code=self.cleaned_data['code'])
        if len(codes):
            codes = Code.objects.filter(phone_number=self.cleaned_data['phone_number'])
            codes.delete()
        else:
            raise forms.ValidationError("Code Not Valid!")
        
        return super().clean()