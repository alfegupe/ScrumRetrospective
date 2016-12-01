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


class UpdateDataUserForm(forms.ModelForm):

    email = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}),
        error_messages={
            'required': 'El email es requerido.',
            'invalid': 'Ingrese un email valido'
        }
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class UpdatePasswordUserForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Password actual'}),
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Nuevo Password'}),
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Repita nuevo Password'}),
    )

    def clean(self):
        pass1 = self.cleaned_data['new_password']
        pass2 = self.cleaned_data['repeat_password']
        if len(pass1) < 5:
            raise forms.ValidationError(
                'El nuevo password debe tener al menos 5 caracteres')
        if pass1 != pass2:
            raise forms.ValidationError('Los passwords no coinciden.')
        return self.cleaned_data