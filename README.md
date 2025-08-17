# 📱 Phone Number Authentication (Django)

A clean, production‑ready Django starter that authenticates **by phone number** (no username or email required).  
It ships with a **custom user model**, a **custom authentication backend** for `phone_number + password`, and modern templates for register, login, profile update, deactivate/reactivate, and delete. Internationalization (i18n) is built‑in, with an **optional** section for `django-modeltranslation` if you also need to translate **database fields**.

> Built and maintained by **Turdiali Xasanbayev (@turdialixasanbayev)** — Backend Developer. PRs and issues are welcome!

---

## ✨ Features

- 🔐 Phone‑number–first auth flow (no username/email)
- 👤 `CustomUser` model with unique `phone_number`
- 🔑 Custom `PhoneBackend` (authenticate via `phone_number + password`)
- 🧭 Templates: Home, Register, Login, Update Profile, Deactivate/Reactivate, Delete
- 🌍 i18n ready (Uzbek/English/Russian/Turkish examples)
- 🧰 Scripts folder for local helpers (make them executable)
- 🧪 Easily extendable: OTP/SMS, DRF API, tests, rate‑limit, etc.

---

## 🗂 Project Structure

```
phone-number-auth/
├─ core/                 # Project settings, urls, wsgi/asgi
├─ users/                # CustomUser model, auth backend, forms/views/urls
├─ templates/            # Server-rendered pages
├─ requirements/         # Requirements (if split by envs)
├─ scripts/              # Local helper scripts (chmod +x after clone)
├─ manage.py
└─ README.md
```

Key places to look at:

- `users/models.py` – `CustomUser` with `phone_number` as the identifier  
- `users/backends.py` – `PhoneBackend` (auth by phone + password)  
- `core/settings.py` – `AUTH_USER_MODEL` & `AUTHENTICATION_BACKENDS` wiring  
- `users/urls.py` & `core/urls.py` – URL configuration (with `i18n_patterns`)  
- `templates/` – clean, minimal UI with language switcher

---

## 🚀 Quickstart

### 1) Clone & create a virtualenv
```bash
git clone https://github.com/turdialixasanbayev/phone-number-auth.git
cd phone-number-auth

# Create & activate venv (Linux/macOS)
python -m venv .venv && source .venv/bin/activate
# On Windows (PowerShell)
# python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```bash
# If a consolidated requirements file exists
pip install -r requirements.txt

# Or, if split by envs:
# pip install -r requirements/base.txt
```

### 3) Environment variables
Create a `.env` in the project root (or set these in your environment):

```dotenv
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=*
```

Ensure these settings exist in `core/settings.py` (they typically already do in this project):
```python
AUTH_USER_MODEL = "users.CustomUser"
AUTHENTICATION_BACKENDS = [
    "users.backends.PhoneBackend",               # phone + password
    "django.contrib.auth.backends.ModelBackend"  # default/admin
]
```

### 4) Migrate & run
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Visit: http://127.0.0.1:8000/

> **Tip:** after cloning, make helper scripts executable:
> ```bash
> chmod 755 scripts/*  # or: chmod +x scripts/*
> ```

---

## 🔐 Creating a superuser

Use your phone number as the unique identifier:
```bash
python manage.py createsuperuser
# Fill prompts (phone_number + password)
```
> Depending on your `CustomUserManager`, you may also be able to pass `--phone_number +998...` from CLI. If not, the interactive prompts will ask for it.

---

## 🔌 How the Phone Backend works

`users/backends.PhoneBackend` usually:

1. Accepts `phone_number` and `password` from the login form
2. Normalizes the phone number (strip spaces, unify format)
3. Fetches the user by `phone_number`
4. Checks password: `user.check_password(password)`
5. Returns the user (or `None`)

**Usage in a view:**
```python
from django.contrib.auth import authenticate, login

user = authenticate(request, phone_number=phone, password=pw)  # routed to PhoneBackend
if user is not None:
    # Avoid "multiple backends" error by specifying the backend explicitly
    login(request, user, backend="users.backends.PhoneBackend")
    # redirect to home
```

**Updating password without logging the user out:**
```python
from django.contrib.auth import update_session_auth_hash

request.user.set_password(new_password)
request.user.save()
update_session_auth_hash(request, request.user)  # keep session alive
```

**Changing phone or password in one form:** simply conditionally set the fields that were provided, then save.

---

## 🌍 Internationalization (i18n)

This project is set up to translate server‑rendered content (templates/messages).

### Settings checklist
```python
# core/settings.py

LANGUAGE_CODE = "en"
TIME_ZONE = "Asia/Tashkent"

LANGUAGES = [
    ("uz", "Uzbek"),
    ("en", "English"),
    ("ru", "Russian"),
    ("tr", "Turkish"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

MIDDLEWARE = [
    # ...
    "django.middleware.locale.LocaleMiddleware",
    # ...
]

TEMPLATES = [
    {
        # ...
        "OPTIONS": {
            "context_processors": [
                # ...
                "django.template.context_processors.i18n",
            ],
        },
    },
]
```

### URL configuration
```python
# core/urls.py
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # set_language endpoint
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += i18n_patterns(
    path("", include("users.urls")),  # localize only site URLs (not admin)
)
```

### Language switcher (template)
```html
<form action="{% url 'set_language' %}" method="post" class="flex items-center space-x-2">
    {% csrf_token %}
    <select name="language"
        class="px-3 py-2 rounded-lg border border-gray-300 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="uz" {% if LANGUAGE_CODE == 'uz' %}selected{% endif %}>🇺🇿 Uzbek</option>
        <option value="en" {% if LANGUAGE_CODE == 'en' %}selected{% endif %}>🇬🇧 English</option>
        <option value="ru" {% if LANGUAGE_CODE == 'ru' %}selected{% endif %}>🇷🇺 Русский</option>
        <option value="tr" {% if LANGUAGE_CODE == 'tr' %}selected{% endif %}>🇹🇷 Türkçe</option>
    </select>
    <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700">
        {% trans "Change" %}
    </button>
</form>
```

### Working with `.po` files
```bash
# Generate messages for multiple languages
django-admin makemessages -l uz -l en -l ru -l tr

# Compile after editing translations
django-admin compilemessages
```

> For static/template strings, use `{% trans "..." %}` or `{% blocktrans %}...{% endblocktrans %}`.

---

## 🧩 Optional: Translating DB fields with `django-modeltranslation`

If you **also** need to translate fields stored in the database (e.g., a `title` or `bio`), you can add `django-modeltranslation`.

1) Install and add to settings:
```bash
pip install django-modeltranslation
```
```python
INSTALLED_APPS = [
    # ...
    "modeltranslation",
]
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = ("uz", "en", "ru", "tr")
```

2) Create `translation.py` in the app with the model you want to translate:
```python
# example: users/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Profile  # example model with a 'bio' field

@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ("bio",)  # will create bio_uz, bio_en, bio_ru, bio_tr
```

3) Make migrations & migrate:
```bash
python manage.py makemigrations
python manage.py migrate
```

> If your project only translates **static template strings**, you can skip `django-modeltranslation` entirely and rely on Django’s built‑in i18n.

---

## 🧱 Endpoints (typical)

> Exact names may vary; check `users/urls.py` in your repo.

- `GET /` — Home
- `GET|POST /users/auth/register/` — Register
- `GET|POST /users/auth/login/` — Login
- `POST /users/auth/logout/` — Logout
- `GET|POST /users/profile/update/` — Update phone/password
- `POST /users/profile/deactivate/` — Deactivate account
- `POST /users/profile/reactivate/` — Reactivate account
- `POST /users/profile/delete/` — Hard delete account

---

## 🔒 Security notes

- Always call `login(request, user, backend="users.backends.PhoneBackend")` after `authenticate(...)` to avoid “multiple backends” issues.
- Normalize phone numbers (e.g., E.164) before lookup to avoid duplicates.
- When changing password, call `update_session_auth_hash(...)` to keep the session.
- Add password validation & rate‑limiting (e.g., `AUTH_PASSWORD_VALIDATORS`, `django-ratelimit`).
- Consider OTP/SMS to verify ownership of the phone number.

---

## 🧪 Extending

- OTP/SMS verification (Twilio, PlayMobile, etc.)
- Password reset via phone (SMS code)
- DRF endpoints for mobile apps
- CI (ruff/black/isort + pytest)
- Docker/Compose for dev
- Admin action: “Verify phone”

---

## 📜 License

Choose a license (MIT is common for open source). Add a `LICENSE` file at the repo root.

---

## 👤 Author

**Turdiali Xasanbayev** — Backend Developer  
GitHub: [@turdialixasanbayev](https://github.com/turdialixasanbayev)

---

## 🙌 Acknowledgements

- Django documentation for Auth & i18n
- Community examples of custom authentication backends

---

## 📎 Appendix

### Make scripts executable
```bash
chmod 755 scripts/*
# or:
chmod +x scripts/*
```