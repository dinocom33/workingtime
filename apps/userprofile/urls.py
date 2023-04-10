from django.urls import path
from apps.userprofile.views import myaccount, edit_profile

urlpatterns = [
    path("myaccount/", myaccount, name="myaccount"),
    path("edit_profile/", edit_profile, name="edit_profile"),
]
