# Phone Number Authentication (Django)

A minimal, production-ready example of authenticating users **by phone number** in Django.  
It ships with a custom user model, a custom authentication backend, and simple templates for sign‑up, log‑in, profile update, and delete.

---

## ✨ Features

- **Phone‑number–first auth flow** (no username/email required).
- **Custom user model** with `phone_number` as the unique identifier.
- **Custom authentication backend** to authenticate via phone + password.
- **CRUD for the profile**: register, login, update password/phone, delete.
- **Server‑rendered templates** for a clean, minimal UI.
- Works out-of-the-box with **SQLite** for local development.

> Note: If you need OTP/SMS verification, you can integrate providers like Twilio or PlayMobile later. This project focuses on password-based login via phone number.

---

## 🧱 Project Structure

```
phone-number-auth/
├─ core/                 # Django project (settings, urls, wsgi/asgi)
├─ users/                # App with CustomUser model, auth backend, forms, views
├─ templates/            # HTML templates (register, login, update, delete, home)
├─ requirements/         # (Optional) requirements files for environments
├─ manage.py
└─ README.md
```

Key parts you’ll likely look for:

- `users/models.py` – `CustomUser` + `CustomUserManager` (`create_user`, `create_superuser`)
- `users/backends.py` – `PhoneBackend` for phone + password authentication
- `core/settings.py` – `AUTH_USER_MODEL` and `AUTHENTICATION_BACKENDS` wiring
- `templates/` – basic forms and navigation (Login / Register / Update / Delete)

---

## 🚀 Quickstart (Local)

### 1) Clone & create a virtual environment
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
pip install -r requirements.txt  # or use requirements/base.txt if provided
# If there is a requirements/ directory with multiple files, use the appropriate one:
# pip install -r requirements/base.txt
```

> If you don’t have a consolidated `requirements.txt`, you can export one later with:
> ```bash
> pip freeze > requirements.txt
> ```

### 3) Environment variables
Create a `.env` in the project root (or set these directly in your environment).

```bash
# .env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=*
```

In `core/settings.py`, make sure these are set (already configured in this project, but shown here for clarity):

```python
AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = [
    "users.backends.PhoneBackend",                         # phone + password
    "django.contrib.auth.backends.ModelBackend",           # admin & default
]
```

### 4) Apply migrations & run
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## 🔑 Creating a Superuser (by phone number)

Use your phone number as the unique identifier:

```bash
python manage.py createsuperuser --phone_number +998901234567
# You will be prompted for a password
```

If your Django prompts are different, it’s because your `CustomUserManager` defines which fields are required for superuser creation. Adjust accordingly (e.g., it may ask interactively).

---

## 🧭 URLs (typical)

> Exact paths may differ slightly based on your `users/urls.py` – below is the expected shape used in templates.

- `GET /` – Home page
- `GET|POST /users/auth/register/` – Register
- `GET|POST /users/auth/login/` – Log in
- `POST /users/auth/logout/` – Log out
- `GET|POST /users/profile/update/` – Update profile (phone or password)
- `POST /users/profile/delete/` – Delete profile

Templates show a header like:

```html
{% if user.is_authenticated %}
  <h1>Welcome, {{ user.phone_number }} 👋</h1>
  <a href="{% url 'logout' %}">Logout</a>
  <a href="{% url 'update' %}">Update Profile</a>
  <a href="{% url 'delete' %}">Delete Profile</a>
{% else %}
  <a href="{% url 'login' %}">Login</a>
  <a href="{% url 'register' %}">Register</a>
{% endif %}
```

---

## 🛠️ How the Phone Backend Works

`users/backends.PhoneBackend` typically does:

1. Accept a `phone_number` and `password` from the login form.
2. Normalize the phone number (strip spaces, optional country code handling).
3. Query `CustomUser` by `phone_number`.
4. Validate `password` with `user.check_password(...)` and return the user.

This allows you to keep all Django auth features (sessions, `login()`, permissions, admin) but key off the phone number instead of a username/email.

---

## 🧪 Common Issues & Fixes

### “You have multiple authentication backends configured…”
**Error:**  
```
ValueError: You have multiple authentication backends configured and therefore must
provide the `backend` argument or set the `backend` attribute on the user.
```
**Why it happens:** Django can’t infer which backend authenticated the user.

**Fix:** Always authenticate with the backend and use that backend when logging in:
```python
from django.contrib.auth import authenticate, login

user = authenticate(request, phone_number=phone, password=pw)  # uses PhoneBackend
if user is not None:
    login(request, user, backend="users.backends.PhoneBackend")
```
Also make sure `AUTHENTICATION_BACKENDS` includes both your phone backend **and** `ModelBackend` (admin fallback).

### Admin login fails with phone number
Use your **superuser phone number** and password. If you added staff via Admin with no password, set one:
```bash
python manage.py changepassword <phone_number>
```

### Phone number format
Be consistent (e.g., E.164: `+998...`). If you accept local formats on forms, normalize to one canonical format in `clean()` or the backend before querying.

---

## 📦 Extending This Project

- **OTP/SMS verification**: add a `PhoneOTP` model and integrate a provider (Twilio/PlayMobile) to send & verify codes.
- **Rate limiting**: throttle login and OTP requests (django-ratelimit).
- **Audit & security**: add login attempt logs, 2FA, and password validation policies.
- **Internationalization**: translate templates and messages.
- **API**: expose DRF endpoints for mobile clients.
- **Testing**: add unit tests for `PhoneBackend` and forms.

---

## 🧰 Tech Stack

- **Python & Django**
- **SQLite** for local development (switch to Postgres/MySQL in production)
- **Django templates** for the UI

---

## 📜 License

Add a `LICENSE` file (MIT is common for open-source). If you intend this to be private or proprietary, specify that clearly.

---

## 🙌 Credits

Built by **@turdialixasanbayev**.  
Contributions, issues and feature requests are welcome!

---

## 🗺️ Roadmap (ideas)

- OTP login + “passwordless” flow
- Password reset by phone (via SMS code)
- Admin action to “Verify phone”
- Dockerfile + Compose for dev
- CI checks (ruff/black/isort + pytest)