from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

class LoginForm(AuthenticationForm):
	username=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'UCSD Email'}))
	password=forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class SignupForm(UserCreationForm):
	username=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'UCSD Email'}))
	password1=forms.CharField(label="", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
	password2=forms.CharField(label="", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Retype Password'}))

class CreateListingForm(forms.Form):
	#renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
	
	# should userID provided by the form?
	title = forms.CharField(max_length=50)
	price = forms.CharField(max_length=20)
	canDeliver = forms.BooleanField(required=False)
	condition = forms.CharField(max_length=10)
	description = forms.CharField(max_length=500, required=False)
	contactInformation = forms.CharField(max_length=20)
	image = forms.ImageField(required=False)
