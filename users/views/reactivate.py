from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model


User = get_user_model()


@login_required
def reactivate_account(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id, status='deactive')
        user.status = 'active'
        user.save()
        messages.success(request, "Your account has been reactivated.")
    except Exception as e:
        messages.error(request, "An error occurred while reactivating your account.")
    return redirect("home")
