from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import TicketForm, DepartmentForm


from .models import Ticket

# Create your views here.


def list_all_tickets(request: HttpRequest):
    tickets = Ticket.objects.all()

    return render(request, "tickets/all.html", {"tickets": tickets})


def list_open_tickets(request: HttpRequest):
    open_tickets = Ticket.objects.filter(status=Ticket.Status.ABERTO)

    return render(request, "tickets/open.html", {"open_tickets": open_tickets})


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
    department_form = DepartmentForm()
    return render(
        request,
        "tickets/create_ticket.html",
        {"form": form, "department_form": department_form},
    )


def create_department(request: HttpRequest):
    if request.method == "POST":
        form_department = DepartmentForm(request.POST)
        if form_department.is_valid():
            form_department.save()
            return render(request, "tickets/department_created.html")
    else:
        form_department = DepartmentForm()

    return render(
        request,
        "tickets/partials/create_department_modal.html",
        {"form_department": form_department},
    )
