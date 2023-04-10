from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from apps.userprofile.models import Userprofile
from django.contrib import messages


def home(request):
    return render(request, "main/home.html")


def privacy(request):
    return render(request, "main/privacy.html")


def terms(request):
    return render(request, "main/terms.html")


def plans(request):
    return render(request, "main/plans.html")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()

            userprofile = Userprofile.objects.create(user=user)
            login(request, user)
            messages.info(request, "You have successfully logged into your account.")
            return redirect("myaccount")
    else:
        form = UserCreationForm

    return render(request, "main/signup.html", {"form": form})
