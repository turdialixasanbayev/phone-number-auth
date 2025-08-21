from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re
from django.shortcuts import redirect, render


@login_required
def update_profile(request):
    if request.method == "POST":
        current_phone = request.POST.get("current_phone_number")
        new_phone = request.POST.get("phone_number")
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        # ✅ Telefon raqam yangilash
        if new_phone:
            # Agar foydalanuvchi current phone_number ham kiritgan bo'lsa
            if current_phone:
                if current_phone != user.phone_number:
                    messages.error(
                        request, "Current phone number is incorrect ❌")
                    return redirect("update")

                if new_phone == user.phone_number:
                    messages.error(
                        request, "New phone number cannot be the same as current phone number ❌")
                    return redirect("update")

            # Telefon raqam formati tekshirish (oddiy misol: faqat raqamlar va +)
            if not re.match(r'^\+?\d{9,15}$', new_phone):
                messages.error(request, "Invalid phone number format ❌")
                return redirect("update")

            # Agar boshqa userda shu raqam mavjud bo'lsa
            from django.contrib.auth import get_user_model

            User = get_user_model()

            if User.objects.exclude(id=user.id).filter(phone_number=new_phone).exists():
                messages.error(request, "This phone number is already taken ❌")
                return redirect("update")

            user.phone_number = new_phone

        # ✅ Parolni yangilash
        if new_password or confirm_password:
            if not current_password:
                messages.error(
                    request, "Please enter your current password to change password ❌")
                return redirect("update")

            if not user.check_password(current_password):
                messages.error(request, "Current password is incorrect ❌")
                return redirect("update")

            if not new_password:
                messages.error(request, "New password cannot be empty ❌")
                return redirect("update")

            if new_password == request.user.password:
                messages.error(
                    request, "New password cannot be the same as current password ❌")
                return redirect("update")

            if len(new_password) < 3:
                messages.error(
                    request, "New password must be at least 3 characters ❌")
                return redirect("update")

            if new_password != confirm_password:
                messages.error(
                    request, "New password and confirm password do not match ❌")
                return redirect("update")

            user.set_password(new_password)
            # Logout bo‘lib qolmaslik uchun
            update_session_auth_hash(request, user)

        # ✅ Foydalanuvchini saqlash
        user.save()
        messages.success(
            request, "Your profile has been updated successfully ✅")
        return redirect("home")

    return render(request, "users/update_profile.html")
