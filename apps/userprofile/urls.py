from django.urls import path
from apps.userprofile.views import myaccount, edit_profile, accept_invitation

urlpatterns = [
    path("myaccount/", myaccount, name="myaccount"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("accept_invitation/", accept_invitation, name="accept_invitation")
]
