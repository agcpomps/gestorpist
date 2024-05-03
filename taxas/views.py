from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.db.models import Q


from .models import Licenca, Contribuinte
from .forms import ContribuinteForm, LicencaForm


def licenca_list(request: HttpRequest):
    licencas = Licenca.objects.all()

    return render(request, "taxas/licenca.html", {"licencas": licencas})


def criar_licenca(request: HttpRequest):
    if request.method == "POST":
        form = LicencaForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/taxas")
    else:
        form = LicencaForm()

    return render(request, "taxas/criarlicenca.html", {"form": form})


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


def search(request: HttpRequest):

    query = request.GET.get("q")

    if query:
        licencas = Licenca.objects.filter(Q(numero__icontains=query))
    return render(request, "taxas/search.html", {"licencas": licencas})
