from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import index
from .views import CustomLoginView

urlpatterns = [
    path('', index, name='index'),
    path('login/', CustomLoginView, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]