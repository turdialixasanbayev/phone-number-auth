from django.urls import path

from users.views.home import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
