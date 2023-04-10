from django.http import HttpResponse
from django.shortcuts import render


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, '403.html', status=403)

        return wrapper_func

    return decorator


def not_allowed_users(not_allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in not_allowed_roles:
                return render(request, '403.html', status=403)
            else:
                return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, '403.html', status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper_function

