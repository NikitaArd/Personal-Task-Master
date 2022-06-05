from django.shortcuts import render


def index(request):
    context = {'user': request.user}
    return render(request, 'taskapp/index.html', context)
