from django.shortcuts import render
from django.shortcuts import redirect
from .forms import (
    LoginForm,
    RegistrationForm
)
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


@login_required()
def index(request):
    context = {'user': request.user}
    return render(request, 'taskapp/index.html', context)


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
                        return redirect('taskapp:index')
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
            return render(request, 'registration/login.html', context)
        else:
            context = {
                'form': ModelFormset,
                'title': 'Login',
                'isInvalid': '',
            }
            return render(request, 'registration/login.html', context)
    else:
        return redirect('taskapp:index')


def CustomRegistrationView(request):

    ModelFormset = RegistrationForm

    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = ModelFormset(request.POST)
            if form.is_valid():
                form.save()
                return redirect('taskapp:login')
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
                return render(request, 'registration/registration.html', context)
        else:
            context = {
                'form': ModelFormset,
                'title': 'Registration',
                'isInvalid': '',
            }
            return render(request, 'registration/registration.html', context)
    else:
        return redirect('taskapp:index')

