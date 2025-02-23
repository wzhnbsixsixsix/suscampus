import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address has been used, please use another email address.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "The passwords entered twice are inconsistent.")
        return cleaned_data


class LoginForm(AuthenticationForm):
    pass


from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser  # 确保 CustomUser 是你的用户模型
import re

#  Use ModelForm to simplify input
class ChangeUsernameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()

        if not username:
            raise forms.ValidationError("Username cannot be empty.")
        if len(username) < 3 or len(username) > 20:
            raise forms.ValidationError("The username must be between 3-20 characters.")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError("Usernames can only contain letters, numbers, and underscores.")
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken, please choose another one.")

        return username


