from django import forms

class LoginForm(forms.Form):
   LOGIN_ID = forms.CharField(max_length = 100)
   PASSWORD = forms.CharField(widget = forms.PasswordInput())