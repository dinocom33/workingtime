from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.team.models import Team, Invitation
from .forms import NewUserForm
from apps.team.utilities import send_invitation_accepted


# def signup(request):
#     if request.method == "POST":
#         form = NewUserForm(request.POST)
#
#         if form.is_valid():
#             user = form.save()
#             user.email = user.username
#             user.save()
#             login(request, user)
#             messages.success(request, "Registration successful.")
#             return redirect("home")
#         messages.error(request, "Unsuccessful registration. Invalid information.")
#     form = NewUserForm()
#     return render(request=request, template_name="userprofile/signup.html",
#                   context={"register_form": form})


@login_required
def myaccount(request):
    teams = request.user.teams.exclude(pk=request.user.userprofile.active_team_id)
    invitations = Invitation.objects.filter(email=request.user.email, status=Invitation.INVITED)

    return render(request, "userprofile/myaccount.html", {"teams": teams, "invitations": invitations})


@login_required
def edit_profile(request):
    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name", "")
        request.user.last_name = request.POST.get("last_name", "")
        request.user.email = request.POST.get("email", "")
        request.user.save()

        messages.info(request, "Your changes were saved successfully")

        return redirect("myaccount")

    return render(request, "userprofile/edit_profile.html")


@login_required()
def accept_invitation(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        invitations = Invitation.objects.filter(code=code, email=request.user.email)

        if invitations:
            invitation = invitations[0]
            invitation.status = Invitation.ACCEPTED
            invitation.save()

            team = invitation.team
            team.members.add(request.user)
            team.save()

            userprofile = request.user.userprofile
            userprofile.active_team_id = team.id
            userprofile.save()

            messages.info(request, 'Invitation has been accepted')

            send_invitation_accepted(team, invitation)

            return redirect('team:team', team_id=team.id)
        else:
            messages.info(request, 'Invitation was not found')
    else:
        return render(request, 'userprofile/accept_invitation.html')
