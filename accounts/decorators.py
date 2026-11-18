from functools import wraps
from django.shortcuts import render


def role_required(allowed_role):
    """
    Restricts view access to users matching `allowed_role`.
    Renders a 403 Forbidden response if an authenticated user tries to access
    another role's route directly via URL.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role != allowed_role:
                return render(request, 'accounts/403.html', status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator