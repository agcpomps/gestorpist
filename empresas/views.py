from django.shortcuts import render
from django.db.models import Q, Sum, Avg
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

import pandas as pd

from .models import Empresa, Alvara
from .forms import EmpresaForm, AlvaraForm


@login_required
def empresas(request):
    empresas = Empresa.objects.all()

    return render(request, "empresas/empresas.html", {"empresas": empresas})


@login_required
def alvara(request):
    alvaras = Alvara.objects.all()

    return render(request, "empresas/alvaras.html", {"alvaras": alvaras})


@login_required
def criar_empresa(request):
    if request.method == "POST":
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/empresas/")
    else:
        form = EmpresaForm()

    return render(request, "empresas/criar.html", {"form": form})


@login_required
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


def dashboard(request: HttpRequest):
    total_empresas = Empresa.objects.count()
    total_alvaras = Alvara.objects.count()
    alvara_total = Alvara.objects.aggregate(total=Sum("valor"))
    alvara_total_valor = alvara_total["total"]

    return render(
        request,
        "empresas/dashboard.html",
        {
            "total_empresas": total_empresas,
            "alvara_total_valor": alvara_total_valor,
            "total_alvaras": total_alvaras,
        },
    )


def export_to_excel(request: HttpRequest):
    alvaras = Alvara.objects.all()

    data = list(alvaras.values())
    df = pd.DataFrame(data)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = "attachment; filename=data.xlsx"

    with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="alvaras")

    return response


# criar com htmx o empresas a um mês do termino
# criar o filtro por data ano e dar o resultado total de cada ano
