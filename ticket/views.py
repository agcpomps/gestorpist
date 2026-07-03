import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseForbidden
from django.db.models import Count, Q
from .forms import TicketForm, TicketUpdateForm, TicketCommentForm, DepartmentForm


from accounts.models import Department

from .models import Ticket

# Create your views here.


@login_required
def departamentos(request: HttpRequest):
    """Tickets grouped by department (module page, ticket sidebar layout)."""
    departments = (
        Department.objects.prefetch_related(
            "department_tickets__user",
            "department_tickets__assigned_to",
        )
        .order_by("name")
    )
    return render(request, "tickets/departamentos.html", {"departments": departments})


@login_required
def dashboard(request: HttpRequest):
    """Statistics for the ticket module."""
    tickets = Ticket.objects.all()
    status_counts = {
        row["status"]: row["total"]
        for row in tickets.values("status").annotate(total=Count("id"))
    }

    por_departamento = (
        Department.objects.annotate(total=Count("department_tickets"))
        .order_by("-total", "name")
    )

    status_labels = [label for _, label in Ticket.Status.choices]
    status_data = [status_counts.get(code, 0) for code, _ in Ticket.Status.choices]

    context = {
        "total": tickets.count(),
        "abertos": status_counts.get(Ticket.Status.ABERTO, 0),
        "em_progresso": status_counts.get(Ticket.Status.EN_PROGRESSO, 0),
        "resolvidos": status_counts.get(Ticket.Status.RESOLVIDO, 0),
        "fechados": status_counts.get(Ticket.Status.FECHADO, 0),
        "por_departamento": por_departamento,
        "status_labels": json.dumps(status_labels),
        "status_data": json.dumps(status_data),
    }
    return render(request, "tickets/dashboard.html", context)


@login_required
def list_all_tickets(request: HttpRequest):
    tickets = Ticket.objects.select_related("user", "department")

    query = request.GET.get("q", "").strip()
    if query:
        tickets = tickets.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(user__username__icontains=query)
            | Q(department__name__icontains=query)
        )

    status = request.GET.get("status", "").strip()
    if status in Ticket.Status.values:
        tickets = tickets.filter(status=status)
    else:
        status = ""

    context = {
        "tickets": tickets,
        "query": query,
        "status": status,
        "status_choices": Ticket.Status.choices,
    }
    return render(request, "tickets/all.html", context)


@login_required
def ticket_detail(request: HttpRequest, pk):
    ticket = get_object_or_404(
        Ticket.objects.select_related("user", "department", "assigned_to"), pk=pk
    )
    can_manage = request.user.manages(ticket.department_id)

    update_form = TicketUpdateForm(instance=ticket)
    comment_form = TicketCommentForm()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update":
            if not can_manage:
                return HttpResponseForbidden("Sem permissão para gerir este ticket.")
            update_form = TicketUpdateForm(request.POST, instance=ticket)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, "Ticket actualizado com sucesso.")
                return redirect("ticket:detail", pk=ticket.pk)
        elif action == "comment":
            comment_form = TicketCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.author = request.user
                comment.save()
                return redirect("ticket:detail", pk=ticket.pk)

    context = {
        "ticket": ticket,
        "can_manage": can_manage,
        "update_form": update_form,
        "comment_form": comment_form,
        "comments": ticket.comments.select_related("author"),
    }
    return render(request, "tickets/detail.html", context)


@login_required
def create_ticket(request: HttpRequest):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("ticket:ticketall")
    else:
        form = TicketForm()
    return render(
        request,
        "tickets/create_ticket.html",
        {"form": form, "form_department": DepartmentForm()},
    )


@login_required
def create_department(request: HttpRequest):
    if not request.user.is_staff:
        return HttpResponseForbidden("Apenas administradores podem criar departamentos.")
    if request.method == "POST":
        form_department = DepartmentForm(request.POST)
        if form_department.is_valid():
            new_department = form_department.save()
            return render(
                request,
                "tickets/department_created.html",
                {
                    "departments": Department.objects.all(),
                    "new_department": new_department,
                },
            )
    else:
        form_department = DepartmentForm()

    return render(
        request,
        "tickets/partials/create_department_modal.html",
        {"form_department": form_department},
    )
