from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .views import index
from .views import CustomLoginView
from .views import CustomRegistrationView
from .views import CustomPasswordChangeView
from .views import CustomPasswordResetConfirmView
from .views import AjaxCreateView
from .views import AjaxUpdateView

from .forms import CustomPasswordResetForm
from .forms import CustomSetPasswordForm

urlpatterns = [
    path('', index, name='index'),
    path('login/', CustomLoginView, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', CustomRegistrationView, name='registration'),
    path('accounts/change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('accounts/reset/', PasswordResetView.as_view(
        template_name='auth_templates/reset_password.html',
        email_template_name='auth_templates/reset_email.txt',
        form_class=CustomPasswordResetForm,
    ), name='password_reset'),
    path('accounts/reset/done', PasswordResetDoneView.as_view(
        template_name='auth_templates/reset_password_done.html',
    ), name='password_reset_done'),
    path('accounts/reset/<str:uidb64>/<str:token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/complete/', PasswordResetCompleteView.as_view(
        template_name='auth_templates/reset_password_complete.html',
    ), name='password_reset_complete'),
    path('taskapp/ajax/create/', AjaxCreateView, name='ajax_create'),
    path('taskapp/ajax/update/<int:pk>', AjaxUpdateView, name='ajax_update')
]
