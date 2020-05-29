from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from authentication.forms import LoginForm
from twitteruser.forms import TwitterUserForm
from twitteruser.models import TwitterUser
from django.template.defaultfilters import slugify


def loginView(request):
    message_after = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get("next", reverse("home")))
            else:
                message_after = """Credentials supplied do not match our records.
                    Please try again."""
    form = LoginForm()
    return render(
        request,
        "../templates/general_form.html",
        {"form": form, "message_after": message_after},
    )


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def signupView(request):
    context = {}
    if request.method == "POST":
        form = TwitterUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = TwitterUser.objects.create(
                username=data["username"],
                password=data["password"],
                display_name=data["display_name"],
                slug=slugify(data["username"]),
            )
            new_user.set_password(raw_password=data["password"])
            new_user.save()
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user:
                login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            context["form"] = form
    else:
        form = TwitterUserForm()
        context["form"] = form
    return render(request, "../templates/general_form.html", context)
