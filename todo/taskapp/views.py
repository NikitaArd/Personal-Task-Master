import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetConfirmView
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone

from .decorators import anonymous_required
from .decorators import is_ajax_request
from .forms import (
    LoginForm,
    RegistrationForm,
    CustomPasswordChangeForm,
    CustomSetPasswordForm,
    TaskAddForm,
)
from .models import CustomUser
from .models import Task

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import CustomPasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages

import smtplib
import os
from email.mime.text import MIMEText

from django.contrib.auth import settings



@login_required
def index(request):
    byUserTasks = Task.objects.filter(byUser=request.user, doneStatus=False)
    byUserTasksDone = Task.objects.filter(byUser=request.user, doneStatus=True)
    context = {
        'form': TaskAddForm,
        'tasks': byUserTasks,
        'tasksDone': byUserTasksDone,
        'user': request.user,
    }
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


@anonymous_required('index')
def CustomLoginView(request):
    ModelFormset = LoginForm
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


@anonymous_required('index')
def CustomRegistrationView(request):
    ModelFormset = RegistrationForm

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


# anonymous required there https://docs.djangoproject.com/en/4.0/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin
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


@is_ajax_request(method='POST')
def AjaxCreateView(request):
    form = TaskAddForm(request.POST)
    if form.is_valid():
        response = form.save(commit=False)
        response.byUser = request.user
        response.save()
        formData = response
        ser_formData = serializers.serialize('json', [formData, ])
        return JsonResponse({'formData': ser_formData}, status=200)
    else:
        return JsonResponse({'error': form.errors}, status=400)


def AjaxUpdateView(request, pk):
    task = Task.objects.get(pk=pk)
    if task.byUser == request.user:
        task.doneStatus = bool(int(request.GET.get('doneFlag')))
        task.date = datetime.datetime.now(tz=timezone.utc)
        task.save()
        ser_response = serializers.serialize('json', [task, ])
        return JsonResponse({'task': ser_response}, status=200)
    else:
        return JsonResponse({}, status=400)


def AjaxDeleteView(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        if task.byUser == request.user:
            task.delete()
            return JsonResponse({}, status=200)
        else:
            return redirect('index')
    except ProtectedError:
        return JsonResponse({}, status=400)
    except ObjectDoesNotExist:
        return redirect('index')


@anonymous_required('index')
def password_reset_request(request):
    if request.method == "POST":
        # Set sender email and sender password
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        # Fill out the form
        password_reset_form = CustomPasswordResetForm(request.POST)
        # If form is invalid (for ex. emailgmail.com ...)
        if password_reset_form.is_valid():
            # Getting email from form
            email = password_reset_form.cleaned_data['email']
            # Check if the user with this email exists
            users = CustomUser.objects.filter(Q(email=email))
            if users.exists():
                user = users[0]
                # Create config for email letter
                subject = "Password Reset Requested"
                email_template_name = "auth_templates/reset_email.txt"
                email_context = {
                    "email": user.email,
                    'domain': settings.ALLOWED_HOSTS[0],
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, email_context)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()

                try:
                    # Sending email
                    server.login(sender, password)
                    msg = MIMEText(email)
                    msg['Subject'] = subject
                    server.sendmail(sender, user.email, msg.as_string())
                    return redirect('password_reset_done')
                except Exception as e:
                    return HttpResponse(f'{e}')
        context = {
            'form': CustomPasswordResetForm,
            'title': 'Incorrect e-mail',
            'isInvalid': 'email',
        }
    else:
        context = {
            'form': CustomPasswordResetForm,
            'title': 'Reset password',
            'isInvalid': '',
        }
    return render(request=request, template_name="auth_templates/reset_password.html",
                  context=context)

