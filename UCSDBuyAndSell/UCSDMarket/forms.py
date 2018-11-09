from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

class LoginForm(AuthenticationForm):
	username=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'UCSD Email'}))
	password=forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class SignupForm(UserCreationForm):
	username=forms.CharField(label="Email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'UCSD Email'}))
	password1=forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
	password2=forms.CharField(label="Retype Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Retype Password'}))
