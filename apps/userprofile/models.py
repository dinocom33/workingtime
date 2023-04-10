import uuid
from django.contrib.auth.models import User
from django.db import models


class Userprofile(models.Model):
    # user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="userprofile", on_delete=models.CASCADE)
    active_team_id = models.IntegerField(default=0)
