from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            if hasattr(request.user, 'profile') and request.user.profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator

def instructor_required(view_func):
    return role_required(['instructor'])(view_func)

def student_required(view_func):
    return role_required(['student'])(view_func)