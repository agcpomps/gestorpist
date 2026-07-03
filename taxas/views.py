from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth
import json

from .models import Licenca, Contribuinte
from .forms import ContribuinteForm, LicencaForm


@login_required
def licenca_list(request: HttpRequest):
    licencas = Licenca.objects.all()

    return render(request, "taxas/licenca.html", {"licencas": licencas})


@login_required
def criar_licenca(request: HttpRequest):
    if request.method == "POST":
        form = LicencaForm(request.POST)
        if form.is_valid():
            licenca = form.save(commit=False)
            licenca.emitido_por = request.user
            licenca.save()
        return HttpResponseRedirect("/taxas")
    else:
        form = LicencaForm()

    return render(request, "taxas/criarlicenca.html", {"form": form})

@login_required
def edit_licenca(request: HttpRequest, pk) -> HttpResponse:
    licenca = get_object_or_404(Licenca, pk=pk)
    if request.GET.get("cancel"):
        return render(request, "taxas/partials/licenca_row.html", {"licenca": licenca})
    if request.method == "POST":
        form = LicencaForm(request.POST,instance=licenca)
        if form.is_valid():
            form.save()
            return render(
                request, "taxas/partials/licenca_row.html", {"licenca": licenca}
            )

        else:
            print(form.errors)
    else:
        form = LicencaForm(instance=licenca)
    
    return render(
        request, "taxas/partials/edit_licenca.html", {"form": form, "licenca": licenca}
    )

@login_required
def delete_licenca(request: HttpRequest, pk) -> HttpResponse:
    
    if request.method == "DELETE":
        licenca = get_object_or_404(Licenca, pk=pk)
        licenca.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=405)




@login_required
def contribuinte_list(request: HttpRequest):
    contribuintes = Contribuinte.objects.all()

    query = request.GET.get("q", "").strip()
    if query:
        contribuintes = contribuintes.filter(
            Q(nome__icontains=query) | Q(nif__icontains=query)
        )

    return render(
        request,
        "taxas/contribuintes.html",
        {"contribuintes": contribuintes, "query": query},
    )

@login_required
def edit_contribuinte(request: HttpRequest, pk) -> HttpResponse:
    contribuinte = get_object_or_404(Contribuinte, pk=pk)
    if request.GET.get("cancel"):
        return render(request, "taxas/partials/contribuinte_row.html", {"contribuinte": contribuinte})
    if request.method == "POST":
        form = ContribuinteForm(request.POST, instance=contribuinte)
        if form.is_valid():
            form.save()
            return render(
                request,
                "taxas/partials/contribuinte_row.html",
                {"contribuinte": contribuinte}
            )
    else:
        form = ContribuinteForm(instance=contribuinte)
    
    return render(
        request,
        "taxas/partials/edit_contribuinte.html",
        {"form": form, "contribuinte": contribuinte}
    )

@login_required
def delete_contribuinte(request: HttpRequest, pk) -> HttpResponse:
    if request.method == "DELETE":
        contribuinte = get_object_or_404(Contribuinte, pk=pk)
        contribuinte.delete()

        return HttpResponse(status=200)
    return HttpResponse(status=405)


@login_required
def criar_contribuinte(request: HttpRequest):
    if request.method == "POST":
        form  = ContribuinteForm(request.POST)
        if form.is_valid():
            contribuinte = form.save(commit=False)
            contribuinte.criado_por = request.user
            contribuinte.save()
        else:
            print(form.errors)
        return redirect("taxas:contribuintes")
    else:
        form = ContribuinteForm()

    return render(request, "taxas/criarcontribuintes.html", {"form": form})


@login_required
def dashboard(request: HttpRequest):
    total_arrecadado = Licenca.objects.aggregate(total=Sum("valor"))["total"] or 0
    total_contribuintes = Contribuinte.objects.count()
    licencas_emitidas = Licenca.objects.count()
    por_distincao = (
        Licenca.objects.values("distincao")
        .annotate(total=Sum("valor"))
    )

    context = {
        "total_arrecadado": total_arrecadado,
        "total_contribuintes": total_contribuintes,
        "licencas_emitidas": licencas_emitidas,
        "por_distincao": por_distincao
    }

    return render(request, "taxas/dashboard.html", context=context)

@login_required
def arrecadacao_mes_licencas_grafico(request: HttpRequest):

    arecadacao_mes = (
        Licenca.objects.filter(data_pagamento__isnull=False)
        .annotate(mes=TruncMonth("data_pagamento"))
        .values("mes")
        .annotate(total=Sum("valor"))
        .order_by("mes")
    )

    label_mes = [a["mes"].strftime("%b %Y") for a in arecadacao_mes]
    valores_mes = [float(a["total"] or 0) for a in arecadacao_mes]

    return render(request, "taxas/partials/grafico_licenca_mes.html", {"label_mes": json.dumps(label_mes), "valores_mes": json.dumps(valores_mes)})


@login_required
def search(request: HttpRequest):
    query = request.GET.get("q", "").strip()
    if not query:
        return redirect("taxas:licenca")

    licencas = Licenca.objects.filter(
        Q(numero__icontains=query)
        | Q(contribuinte__nome__icontains=query)
        | Q(benificiario__icontains=query)
    ).select_related("contribuinte")

    return render(request, "taxas/search.html", {"licencas": licencas, "query": query})
