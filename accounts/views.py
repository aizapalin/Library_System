from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.role == 'librarian':
            return redirect('book_management:index')
        return redirect('book_management:index')