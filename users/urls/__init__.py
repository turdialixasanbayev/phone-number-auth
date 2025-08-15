from django.urls import path, include


urlpatterns = [
    path(
        'auth/',
        include('users.urls.auth')
    ),
    path(
        'base/',
        include('users.urls.base')
    ),
    path(
        'settings/',
        include('users.urls.settings')
    )
]
