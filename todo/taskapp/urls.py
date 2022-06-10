from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView

from .views import index
from .views import CustomLoginView
from .views import CustomRegistrationView
from .views import CustomPasswordChangeView

from .forms import CustomPasswordChangeForm

app_name = 'taskapp'

urlpatterns = [
    path('', index, name='index'),
    path('login/', CustomLoginView, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', CustomRegistrationView, name='registration'),
    path('accounts/change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
