from django.shortcuts import render
from django.shortcuts import redirect
from .forms import LoginForm
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
    context = {}
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
                        return redirect('/')
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

            return render(request, 'registration/login.html', context)
        else:
            context = {
                'form': ModelFormset,
                'title': 'Login',
                'isInvalid': '',
            }
            return render(request, 'registration/login.html', context)
    else:
        return redirect('/')
