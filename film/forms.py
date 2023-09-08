from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username']


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        exclude = ['user']  # ekranin tvyalner@ cherevalu hamar


class UpdFilms(forms.ModelForm):
    class Meta:
        model = Film
        exclude = ['user']


class NotForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text','star']
