from django.urls import path

from ..views.delete import delete_account
from ..views.update import update_profile
from ..views.deactivate import deactivate_account
from ..views.reactivate import reactivate_account


urlpatterns = [
    path("profile/delete/", delete_account, name="delete"),
    path("profile/update/", update_profile, name="update"),
    path("profile/deactivate/", deactivate_account, name="deactivate"),
    path("profile/reactivate/<int:user_id>/",
        reactivate_account, name="reactivate"),
]
