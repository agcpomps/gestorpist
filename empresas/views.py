from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpRequest

from .models import Empresa, Alvara
from .forms import EmpresaForm, AlvaraForm


def empresas(request):
    empresas = Empresa.objects.all()

    return render(request, "empresas/empresas.html", {"empresas": empresas})


def alvara(request):
    alvaras = Alvara.objects.all()

    return render(request, "empresas/alvaras.html", {"alvaras": alvaras})


def criar_empresa(request):
    if request.method == "POST":
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/empresas/")
    else:
        form = EmpresaForm()

    return render(request, "empresas/criar.html", {"form": form})


def criar_alvara(request):
    if request.method == "POST":
        form = AlvaraForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/empresas/alvaras")
    else:
        form = AlvaraForm()
    return render(request, "empresas/alvaracriar.html", {"form": form})


def search_empresa(request: HttpRequest):
    query = request.GET.get("q")

    if query:
        empresas = Empresa.objects.filter(Q(nome__icontains=query))

    return render(request, "empresas/search.html", {"empresas": empresas})
