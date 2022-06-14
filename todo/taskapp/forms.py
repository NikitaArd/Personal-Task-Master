from django.contrib.auth.forms import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from .models import CustomUser
from .models import Task


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


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='E-mail')
    email.widget.attrs.update({'type': 'email',
                               'class': 'form-control dialogWindow-input',
                               'id': 'floatingInput',
                               'required': 'required',
                               'placeholder': 'name@example.com'})

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'form-control dialogWindow-input',
               'id': 'floatingPassword',
               'required': 'required',
               'placeholder': 'Password1'}))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'form-control dialogWindow-input',
               'id': 'floatingPassword',
               'required': 'required',
               'placeholder': 'Password2'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'form-control dialogWindow-input',
               'id': 'floatingPassword',
               'required': 'required',
               'placeholder': 'PasswordOld'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'form-control dialogWindow-input',
               'id': 'floatingPassword',
               'required': 'required',
               'placeholder': 'PasswordNew1'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'form-control dialogWindow-input',
               'id': 'floatingPassword',
               'required': 'required',
               'placeholder': 'PasswordNew2'}))

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='E-mail')
    email.widget.attrs.update({'type': 'email',
                               'class': 'form-control dialogWindow-input',
                               'id': 'floatingInput',
                               'required': 'required',
                               'placeholder': 'name@example.com'})

    class Meta:
        fields = ['email']


class CustomSetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'form-control dialogWindow-input',
               'id': 'floatingPassword',
               'required': 'required',
               'placeholder': 'PasswordNew1'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': 'password',
               'class': 'form-control dialogWindow-input',
               'id': 'floatingPassword',
               'required': 'required',
               'placeholder': 'PasswordNew2'}))

    class Meta:
        fields = ['new_password1', 'new_password2']


class TaskAddForm(ModelForm):
    title = forms.CharField(max_length=400)
    title.widget.attrs.update({
        'type': 'text',
        'placeholder': 'Entere there your plan',
        'class': 'add-input',
        'id': 'add_title',
    })

    class Meta:
        model = Task
        fields = ['title']
