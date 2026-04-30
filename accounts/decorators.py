from django.core.exceptions import PermissionDenied

def librarian_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Allow entry if marked staff/superuser or explicitly librarian role.
        if request.user.is_staff or request.user.is_superuser or getattr(request.user, 'role', None) == 'librarian':
            return view_func(request, *args, **kwargs)
        
        # Otherwise, block them (Minimal access for members)
        raise PermissionDenied
    return wrapper