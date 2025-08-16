from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from users.forms.login import PhoneLoginForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = PhoneLoginForm

    def get_success_url(self):
        return reverse_lazy("home")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")
