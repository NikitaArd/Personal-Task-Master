from django.urls import path
from .views import index
from .views import CustomLoginView

urlpatterns = [
    path('', index, name='index'),
    path('login/', CustomLoginView, name='login'),
]