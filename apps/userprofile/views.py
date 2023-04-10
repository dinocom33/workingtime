from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewUserForm


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
    return render(request, "userprofile/myaccount.html")


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
