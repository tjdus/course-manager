from functools import wraps

from django.http import HttpResponseForbidden

from core.models import UserRole


def get_user_role(user):
    user_role= UserRole.objects.get(user__id = user.id)
    return user_role.role

def has_permission(perm_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                user_role = get_user_role(user)
                if user_role and user_role.permissions.filter(name=perm_name).exists():
                    return view_func(self, request, *args, **kwargs)
            return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator