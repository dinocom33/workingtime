from django.urls import path
from .views import team, add_team, edit_team, activate_team

app_name = "team"

urlpatterns = [
    path("add_team/", add_team, name="add_team"),
    path("edit_team/", edit_team, name="edit_team"),
    path("activate_team/<int:team_id>", activate_team, name="activate_team"),
    path("<int:team_id>/", team, name="team"),
]
