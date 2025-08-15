from django import forms
from django.contrib.auth.forms import AuthenticationForm


class PhoneLoginForm(AuthenticationForm):
    username = forms.CharField(label="Phone Number", max_length=15)

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This user is blocked.", code='inactive')
