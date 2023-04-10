from django.urls import path
from .views import add_team

app_name = "team"

urlpatterns = [
    path("add_team/", add_team, name="add_team")
]