from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from ..forms.register import RegisterForm
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
