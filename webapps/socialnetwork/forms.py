from django import forms
from django.contrib.auth.models import User
from .models import *

class RegistrationForm(forms.Form):
	username = forms.CharField(max_length = 20)
	password1 = forms.CharField(max_length = 200,
								label = 'Password',
								widget = forms.PasswordInput())
	password2 = forms.CharField(max_length = 200,
								label = 'Password',
								widget = forms.PasswordInput())		
	
	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match")
		return cleaned_data
	
	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact = username):
			raise forms.ValidationError("Username is already taken")
		return username

class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		exclude = ('user',)
		widgets = {
			'first_name': forms.TextInput(attrs = {'class': 'form-control'}),
			'last_name': forms.TextInput(attrs = {'class': 'form-control'}),
			'age': forms.NumberInput(attrs = {'class': 'form-control'}),
			'photo': forms.FileInput(),
			'bio': forms.Textarea(attrs = {'class': 'form-control', 
											'row': '4'}),
		}
