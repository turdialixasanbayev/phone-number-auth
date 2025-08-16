from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout


@login_required
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()  # HARD DELETE
    messages.success(request, "Your account has been permanently deleted.")
    return redirect("home")
