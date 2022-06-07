from django.contrib.auth.forms import forms
from django.forms import ModelForm
from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    email.widget.attrs.update({'type': 'email',
                               'class': 'form-control dialogWindow-input',
                               'id': 'floatingInput',
                               'required': 'required',
                               'placeholder': 'name@example.com'})

    password = forms.CharField(widget=forms.PasswordInput(
                               attrs={'type': 'password',
                                      'class': 'form-control dialogWindow-input',
                                      'id': 'floatingPassword',
                                      'required': 'required',
                                      'placeholder': 'Password'}))

    error_css_style = 'is_invalid'

    class Meta:
        fields = ['email', 'password']
