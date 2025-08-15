from django.urls import path

from ..views.delete import delete_account
from ..views.update import update_profile


urlpatterns = [
    path("delete/", delete_account, name="delete"),
    path("update/", update_profile, name="update")
]
