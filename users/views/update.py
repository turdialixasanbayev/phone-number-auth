from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


@login_required
def update_profile(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        user = request.user

        if phone_number:
            user.phone_number = phone_number

        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)

        user.save()

        messages.success(request, "Your profile has been updated successfully ✅")
        return redirect("home")

    return render(request, "users/update_profile.html")
