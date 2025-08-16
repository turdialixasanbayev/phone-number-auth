from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout


@login_required
def deactivate_account(request):
    request.user.status = 'deactive'
    request.user.save()
    logout(request)
    messages.success(request, "Your account has been deactivated.")
    return redirect("home")
