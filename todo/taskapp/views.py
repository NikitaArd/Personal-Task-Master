from django.shortcuts import render


def index(request):
    return render(request, 'taskapp/index.html', {})
