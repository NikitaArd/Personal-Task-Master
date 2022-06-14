from django.shortcuts import redirect


def anonymous_required(redirect_field_name):
    def actual_decorator(func, *args, **kwargs):
        def wrapper(request):
            if request.user.is_authenticated:
                return redirect(redirect_field_name)
            return func(request, *args, **kwargs)
        return wrapper

    return actual_decorator
