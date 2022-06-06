from django.shortcuts import render
from django.shortcuts import redirect
from .forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login


def index(request):
    context = {'user': request.user}
    return render(request, 'taskapp/index.html', context)


def CustomLoginView(request):
    ModelFormset = LoginForm
    context = {}
    if not request.user.is_authenticated:
        if request.method == 'POST':
            emailReq = request.POST.get('email')
            passwordReq = request.POST.get('password')
            user = authenticate(email=emailReq, password=passwordReq)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                context = {
                    'form': ModelFormset,
                    'title': 'Check your password or login',
                    'valid': 'is_invalid',
                }
                return render(request, 'registration/login.html', context)
        else:
            context = {
                'form': ModelFormset,
                'title': 'Login',
                'valid': '',
            }
            return render(request, 'registration/login.html', context)
    else:
        return redirect('/')
