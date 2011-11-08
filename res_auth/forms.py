from django import forms
from django.core.exceptions import ValidationError

def validate_barcode(value):
	valid = True
	
	if len(value) != 14:
		valid = False
	elif not value.isdigit():
		valid = False
		
	if not valid:
		raise ValidationError('Invalid card number.')

class LoginForm(forms.Form):
	barcode = forms.CharField(max_length=100,validators=[validate_barcode,])