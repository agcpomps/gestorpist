import json
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render, get_object_or_404, redirect

from .models import Taxa, Contribuinte
from .forms import TaxaForm, ContribuinteForm


@login_required
def taxas_pagamentos(request):
    taxas = Taxa.objects.all()

    return render(
        request,
        "gupagamentos/pagamentos.html",
        {"taxas": taxas},
    )


@login_required
def contribuintes_list(request: HttpRequest):
    contribuintes = Contribuinte.objects.all()

    query = request.GET.get("q", "").strip()
    if query:
        contribuintes = contribuintes.filter(
            Q(nome__icontains=query) | Q(nif__icontains=query)
        )

    if request.method == "POST":
        form = ContribuinteForm(request.POST)

        if form.is_valid():
            contribuinte = form.save(commit=False)
            contribuinte.criado_por = request.user
            contribuinte.save()
            messages.success(request, f"O {contribuinte.nome} foi criado com sucesso!")
            return redirect("/gupagamentos/contribuintes")
        else:
            messages.error(request, "Erro ao salvar o contribuinte. Verifique os campos e tente novamente.")
    else:

        form = ContribuinteForm()


    return render(
        request,
        "gupagamentos/contribuintes.html",
        {"contribuintes": contribuintes, "form": form, "query": query},
    )

@login_required
def edit_contribuinte(request: HttpRequest, pk) -> HttpResponse:
    contribuinte = get_object_or_404(Contribuinte, pk=pk)
    if request.GET.get("cancel"):
        return render(request, "gupagamentos/partials/contribuinte_row.html", {"contribuinte": contribuinte})

    if request.method == "POST":
        form = ContribuinteForm(request.POST, instance=contribuinte)
        if form.is_valid():
            form.save()
            return render(
                request, 
                "gupagamentos/partials/contribuinte_row.html",
                {"contribuinte": contribuinte}
            )
    else:
        form = ContribuinteForm(instance=contribuinte)

    return render(
        request,
        "gupagamentos/partials/edit_contribuinte.html",
        {"form": form, "contribuinte": contribuinte}
    )

@login_required
def delete_contribuinte(request: HttpRequest, pk):
    if request.method == "DELETE":
        contribuinte = get_object_or_404(Contribuinte, pk=pk)
        contribuinte.delete()
        messages.success(request, f"O {contribuinte.nome} foi deletado!")
        return redirect("/gupagamentos/contribuintes")
    return HttpResponse(status=405)

    



@login_required
def criar_pagamento(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TaxaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, f"Pagamento criado com successo")
            return HttpResponseRedirect("/gupagamentos")
        else:
            messages.error(request, "Erro ao criar o pagamento.")
    else:
        form = TaxaForm()

    return render(request, "gupagamentos/criarpagamentos.html", {"form": form})

@login_required
def delete_pagamento(request: HttpRequest, pk) -> HttpResponse:
    if request.method == "DELETE":
        taxa = get_object_or_404(Taxa, pk=pk)
        taxa.delete()
        messages.success(request, f"O pagamento {taxa.titulo} do {taxa.contribuinte} foi deletado!")
        return redirect("gupagamentos:taxas")
    return HttpResponse(status=405)

@login_required
def editar_pagamento(request: HttpRequest, pk) -> HttpResponse:
    pagamento = get_object_or_404(Taxa, pk=pk)
    if request.GET.get("cancel"):
        return render(request, "gupagamentos/partials/pagamento_row.html", {"pagamento": pagamento})

    if request.method == "POST":
        form = TaxaForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            return render(request, "gupagamentos/partials/pagamento_row.html", {'pagamento': pagamento})
    else:
        form = TaxaForm(instance=pagamento)

    return render(request, "gupagamentos/partials/edit_pagamento.html", {'form': form, 'pagamento': pagamento})

@login_required
def criar_contribuinte(request: HttpRequest):
    if request.method == "POST":
        form = ContribuinteForm(request.POST)

        if form.is_valid():
            contribuinte = form.save(commit=False)
            contribuinte.criado_por = request.user
            contribuinte.save()
            print("FORM VALID - redirecting")
            print(form.errors)
            return redirect("gupagamentos:contribuintes")
        print("FORM ERRORS:", form.errors)
    else:
        form = ContribuinteForm()
    
    return render(request, "gupagamentos/criarcontribuinte.html", {"form": form})


@login_required
def dashboard(request: HttpRequest):
    total_pago = (
        Taxa.objects.aggregate(total=Sum("valor_pago"))["total"] or 0
    )

    total_contrato = (
        Taxa.objects.aggregate(total=Sum("valor_contrato"))["total"] or 0
    )

    diferenca = total_contrato - total_pago

    total_contribuintes = Contribuinte.objects.count()

    total_taxas = Taxa.objects.count()

    ticket_medio = total_pago / total_taxas if total_taxas > 0 else 0

    

    context = {
        "total_pago": total_pago,
        "total_contrato": total_contrato,
        "diferenca": diferenca,
        "total_contribuintes": total_contribuintes,
        "total_taxas": total_taxas,
        "ticket_medio": ticket_medio,
        
    }


    return render(
        request,
        "gupagamentos/dashboard.html",
        context=context
    )

@login_required
def grafico_pagamentos_mes(request: HttpRequest):
    pagamentos_por_mes = (
        Taxa.objects.filter(data_pagamento__isnull=False)
        .annotate(mes=TruncMonth("data_pagamento"))
        .values("mes")
        .annotate(total=Sum("valor_pago"))
        .order_by("mes")
    )

    labels = [p["mes"].strftime("%b %Y") for p in pagamentos_por_mes]
    data = [float(p["total"] or 0) for p in pagamentos_por_mes]

    return render(request, "gupagamentos/partials/grafico_pagamento_mes.html", {"labels": json.dumps(labels), "data": json.dumps(data)})


@login_required
def search_pagamentos(request: HttpRequest):
    query = request.GET.get("q", "").strip()
    if not query:
        return redirect("gupagamentos:taxas")

    taxas = Taxa.objects.filter(
        Q(titulo__icontains=query)
        | Q(contribuinte__nome__icontains=query)
        | Q(contribuinte__nif__icontains=query)
    ).select_related("contribuinte")

    return render(request, "gupagamentos/search.html", {"taxas": taxas, "query": query})
