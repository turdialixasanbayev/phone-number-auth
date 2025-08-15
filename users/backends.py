from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class PhoneBackend(ModelBackend):
    """
    Authenticate user by phone number instead of username.
    """
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        print("📞 PhoneBackend ishlayapti!")

        try:
            user = UserModel.objects.get(phone_number=phone_number)
            print(f"🔍 Topilgan foydalanuvchi: {user}")

        except UserModel.DoesNotExist:
            print("❌ Bunday telefon raqamli foydalanuvchi yo'q")
            return None

        if user.check_password(password):
            print("✅ Parol to'g'ri!")
            return user
        else:
            print("❌ Parol noto'g'ri")
        return None
