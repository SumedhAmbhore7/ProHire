from django.shortcuts import redirect

def hr_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if hasattr(request.user, 'hrprofile'):
            return view_func(request, *args, **kwargs)
        else:
            # Optionally redirect to a specific error page or home
            return redirect('home')
    return wrapper_func
