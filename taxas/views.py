from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect


from .models import Licenca, Contribuinte
from .forms import ContribuinteForm


def licenca_list(request: HttpRequest):
    licencas = Licenca.objects.all()

    return render(request, "taxas/licenca.html", {"licencas": licencas})


def contribuinte_list(request: HttpRequest):
    contribuintes = Contribuinte.objects.all()

    return render(request, "taxas/contribuintes.html", {"contribuintes": contribuintes})


def criar_contribuinte(request: HttpRequest):
    if request.method == "POST":
        form = ContribuinteForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/taxas/contribuintes/")
    else:
        form = ContribuinteForm()

    return render(request, "taxas/criarcontribuintes.html", {"form": form})
