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
from .views import AjaxDeleteView
from .views import password_reset_request

from .forms import CustomPasswordResetForm
from .forms import CustomSetPasswordForm

urlpatterns = [
    path('', index, name='index'),
    # Auth
    path('login/', CustomLoginView, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', CustomRegistrationView, name='registration'),
    path('accounts/change/', CustomPasswordChangeView.as_view(), name='password_change'),
    # Password reset urls
    path('accounts/reset/', password_reset_request, name='password_reset'),
    path('accounts/reset/done', PasswordResetDoneView.as_view(
        template_name='auth_templates/reset_password_done.html',
    ), name='password_reset_done'),
    path('accounts/reset/<str:uidb64>/<str:token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/complete/', PasswordResetCompleteView.as_view(
        template_name='auth_templates/reset_password_complete.html',
    ), name='password_reset_complete'),
    # Create tasks
    path('taskapp/ajax/create/', AjaxCreateView, name='ajax_create'),
    path('taskapp/ajax/update/<int:pk>/', AjaxUpdateView, name='ajax_update'),
    path('taskapp/ajax/delete/<int:pk>/', AjaxDeleteView, name='ajax-delete'),
]
