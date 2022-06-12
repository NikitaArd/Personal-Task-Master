from django.shortcuts import render
from django.shortcuts import redirect
from .forms import (
    LoginForm,
    RegistrationForm,
    CustomPasswordChangeForm,
    CustomSetPasswordForm,
)
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetConfirmView


@login_required()
def index(request):
    context = {'user': request.user}
    return render(request, 'taskapp/index.html', context)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'auth_templates/change_password.html'
    form_class = CustomPasswordChangeForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            keys = [key for key in context['form'].errors.as_data()]
            errorMessages = []
            for fields in context['form'].errors:
                errorMessages.append(context['form'].errors[fields])

            context['title'] = errorMessages[0][0]
            context['isInvalid'] = keys[0]

        return context


def CustomLoginView(request):
    ModelFormset = LoginForm
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = ModelFormset(request.POST)
            if form.is_valid():
                emailReq = form.cleaned_data['email']
                passwordReq = form.cleaned_data['password']
                if CustomUser.objects.filter(email=emailReq).exists():
                    user = authenticate(email=emailReq, password=passwordReq)
                    if user is not None:
                        login(request, user)
                        return redirect('index')
                    else:
                        context = {
                            'form': form,
                            'title': 'Wrong password',
                            'isInvalid': 'password',
                        }
                else:
                    context = {
                        'form': form,
                        'title': 'Wrong e-mail',
                        'isInvalid': 'email',
                    }
            else:
                context = {
                    'form': form,
                    'title': 'Incorrect e-mail',
                    'isInvalid': 'email',
                }
            return render(request, 'auth_templates/login.html', context)
        else:
            context = {
                'form': ModelFormset,
                'title': 'Login',
                'isInvalid': '',
            }
            return render(request, 'auth_templates/login.html', context)
    else:
        return redirect('index')


def CustomRegistrationView(request):
    ModelFormset = RegistrationForm

    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = ModelFormset(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
            else:
                keys = [key for key in form.errors.as_data()]
                errorMessages = []
                for fields in form.errors:
                    errorMessages.append(form.errors[fields])
                context = {
                    'form': form,
                    'title': errorMessages[0][0],
                    'isInvalid': keys[0],
                }
                return render(request, 'auth_templates/registration.html', context)
        else:
            context = {
                'form': ModelFormset,
                'title': 'Registration',
                'isInvalid': '',
            }
            return render(request, 'auth_templates/registration.html', context)
    else:
        return redirect('index')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'auth_templates/reset_password_confirm.html'
    form_class = CustomSetPasswordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            keys = [key for key in context['form'].errors.as_data()]
            errorMessages = []
            for fields in context['form'].errors:
                errorMessages.append(context['form'].errors[fields])

            context['title'] = errorMessages[0][0]
            context['isInvalid'] = keys[0]

        return context
