from django.shortcuts import redirect
from django.http import JsonResponse


def anonymous_required(redirect_field_name):
    def actual_decorator(func, *args, **kwargs):
        def wrapper(request):
            if request.user.is_authenticated:
                return redirect(redirect_field_name)
            return func(request, *args, **kwargs)

        return wrapper

    return actual_decorator


def is_ajax_request(method):
    def actual_decorator(func, *args, **kwargs):
        def wrapper(request):
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == method:
                return func(request, *args, **kwargs)

            return JsonResponse({'error': ""}, status=400)

        return wrapper

    return actual_decorator
