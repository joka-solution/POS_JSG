from django.db import models
from django import forms
from django.contrib.admin import widgets
from .models import User

class create_userForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',  'is_vendedor', 'is_supervisor', 'is_gerente', 'is_patron', 'password']
