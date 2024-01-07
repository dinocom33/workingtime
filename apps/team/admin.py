from django.contrib import admin
from .models import Team, Invitation


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'count_members', 'created_by', 'created_at']
    list_filter = ['title', 'members', 'status', 'created_by', 'created_at']
    search_fields = ['title', 'members', 'status', 'created_by', 'created_at']

    def count_members(self, obj):
        return obj.members.count()


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['email', 'code', 'status', 'date_sent']
    list_filter = ['email', 'status', 'date_sent']
    search_fields = ['email', 'status', 'date_sent']


# admin.site.register(Team)
# admin.site.register(Invitation)
