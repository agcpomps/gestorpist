from django.http import HttpResponseRedirect, HttpRequest
from django.db.models import Q
from django.shortcuts import render

from .models import Taxa, Contribuinte
from .forms import TaxaForm, ContribuinteForm


def taxas_pagamentos(request):
    taxas = Taxa.objects.all()

    return render(
        request,
        "gupagamentos/pagamentos.html",
        {"taxas": taxas},
    )


def contribuintes_list(request):
    contribuintes = Contribuinte.objects.all()

    return render(
        request, "gupagamentos/contribuintes.html", {"contribuintes": contribuintes}
    )


def criar_pagamento(request):
    if request.method == "POST":
        form = TaxaForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/gupagamentos/contribuintes")
    else:
        form = TaxaForm()

    return render(request, "gupagamentos/criarpagamentos.html", {"form": form})


def criar_contribuinte(request):
    if request.method == "POST":
        form = ContribuinteForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/gupagamentos/")
    else:
        form = ContribuinteForm()

    return render(request, "gupagamentos/criarcontribuinte.html", {"form": form})


def search_pagamentos(request: HttpRequest):
    query = request.GET.get("q")

    if query:
        taxas = Taxa.objects.filter(Q(titulo__icontains=query))

    return render(request, "gupagamentos/search.html", {"taxas": taxas})
