from django import forms
from django.contrib.auth.models import User
from babysittingapp.models import UserProfile,Sits
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):

    class Meta:
    	model = UserProfile
    	fields = ('balance',)

class ActivityForm(forms.ModelForm):
	sitting = forms.ModelChoiceField(queryset = User.objects.all())
	date = forms.DateField(widget=DateInput())
	class Meta:
		model = Sits
		fields = ('cost','sitting','date')
