from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    ACTIVE = "active"
    DELETED = "deleted"

    CHOICES_STATUS = (
        (ACTIVE, "Active"),
        (DELETED, "Deleted"),
    )

    title = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name="teams")
    created_by = models.ForeignKey(User, related_name="created_teams", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

