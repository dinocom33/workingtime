import random
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Invitation
from django.contrib.auth.decorators import login_required
from .utilities import send_invitation, send_invitation_accepted


@login_required(login_url='login')
def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    invitations = team.invitations.filter(status=Invitation.INVITED)

    return render(request, "team/team.html", {'team': team, 'invitations': invitations})


@login_required(login_url='login')
def activate_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    userprofile = request.user.userprofile
    userprofile.active_team_id = team_id
    userprofile.save()

    messages.info(request, "The team has been activated")

    return redirect("team:team", team_id=team_id)


@login_required(login_url='login')
def edit_team(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE, members__in=[request.user])
    if request.method == 'POST':
        title = request.POST.get("title")

        if title:
            team.title = title
            team.save()

            messages.info(request, "The changes have been saved successfully")

            return redirect("team:team", team_id=team.id)

    return render(request, "team/edit_team.html", {"team": team})


@login_required(login_url='login')
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


@login_required(login_url='login')
def invite(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE, members__in=[request.user])

    if request.method == "POST":
        email = request.POST.get('email')

        if email:
            invitations = Invitation.objects.filter(team=team, email=email)

            if not invitations:
                code = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789") for i in range(4))
                invitation = Invitation.objects.create(team=team, email=email, code=code)

                messages.info(request, "The user has been invited")

                send_invitation(email, code, team)

                return redirect('team:team', team_id=team.id)
            else:
                messages.info(request, "The user has already been invited")

    return render(request, 'team/invite.html', {'team': team})
