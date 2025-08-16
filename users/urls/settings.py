from django.urls import path

from ..views.delete import delete_account
from ..views.update import update_profile
from ..views.deactivate import deactivate_account
from ..views.reactivate import reactivate_account


urlpatterns = [
    path("delete/", delete_account, name="delete"),
    path("update/", update_profile, name="update"),
    path("deactivate/", deactivate_account, name="deactivate"),
    path("reactivate/<int:user_id>/", reactivate_account, name="reactivate"),
]
