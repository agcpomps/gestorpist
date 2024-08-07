from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, authenticate


from .forms import LoginForm


def home_login_page(request: HttpRequest):
    form = LoginForm()
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("pages:departamentos")
            else:
                form.add_error(None, "Nome de usuario errado ou a password")
        else:
            form.add_error(None, "Nome de  Usuário errado ou a Password")

    else:
        form = LoginForm()

    return render(request, "home.html", context={"form": form, "message": message})


def show_departamentos(request: HttpRequest):
    return render(request, "departamentos.html")
