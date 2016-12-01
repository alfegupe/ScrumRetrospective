# -*- encoding: utf-8 -*-

from django import forms
from models import *

"""
Classes
"""


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Contraseña'}),
    )
