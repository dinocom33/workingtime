from django.shortcuts import render, redirect
from .models import Team
from django.contrib.auth.decorators import login_required


@login_required
def add_team(request):
    if request.method == 'POST':
        title = request.POST.get("title")

        if title:
            team = Team.objects.create(title=title, created_by=request.user)
            team.members.add(request.user)
            team.save()

            userprofile = request.user.userprofile
            userprofile.active_team_id = team.id
            userprofile.save()

            return redirect("myaccount")

    return render(request, "team/add_team.html")
