from django.contrib import admin

# Register your models here.

from .models import Userprofile


@admin.register(Userprofile)
class UserprofileAdmin(admin.ModelAdmin):
    list_display = ['user', 'active_team_id']
    list_filter = ['user__username', 'active_team_id']
    search_fields = ['user__username']

# admin.site.register(Userprofile)
