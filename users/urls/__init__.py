from django.urls import path, include


urlpatterns = [
    path(
        '',
        include('users.urls.auth')
    ),
    path(
        '',
        include('users.urls.base')
    ),
    path(
        '',
        include('users.urls.profile')
    )
]
