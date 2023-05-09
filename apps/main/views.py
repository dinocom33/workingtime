from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from apps.main.decorators import unauthenticated_user, allowed_users, admin_only
from apps.team.models import Invitation
from apps.userprofile.models import Userprofile
from django.contrib import messages
from django.contrib.auth.models import Group


def home(request):
    return render(request, "main/home.html")


def privacy(request):
    return render(request, "main/privacy.html")


def terms(request):
    return render(request, "main/terms.html")


def plans(request):
    return render(request, "main/plans.html")


@login_required(login_url='login')
@admin_only
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.email = user.username
            group = Group.objects.get(name='team_member')
            user.groups.add(group)
            user.save()

            messages.success(request, 'Account was created for ' + user.username)

            userprofile = Userprofile.objects.create(user=user)

            return render(request, "main/signup.html")

            # return redirect("dashboard")
    #         login(request, user)
    #
    #         messages.success(request, "You have successfully logged into your account.")
    #
    #         invitations = Invitation.objects.filter(email=user.email, status=Invitation.INVITED)
    #         if invitations:
    #             return redirect('accept_invitation')
    #         else:
    #             return redirect("dashboard")
    else:
        form = UserCreationForm

    return render(request, "main/signup.html", {"form": form})


@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            messages.success(request, "You have successfully logged into your account.")

            invitations = Invitation.objects.filter(email=user.email, status=Invitation.INVITED)
            if invitations:
                return redirect('accept_invitation')
            else:
                return redirect("myaccount")
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'main/login.html')
