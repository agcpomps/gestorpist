from django.urls import path

from .views import (
    list_all_tickets,
    ticket_detail,
    create_ticket,
    create_department,
    departamentos,
    dashboard,
)


app_name = "ticket"

urlpatterns = [
    path("departamentos", departamentos, name="departamentos"),
    path("estatistica", dashboard, name="dashboard"),
    path("", list_all_tickets, name="ticketall"),
    path("<int:pk>/", ticket_detail, name="detail"),
    path("criar", create_ticket, name="create_ticket"),
    path("criar-departamento", create_department, name="create_department"),
]
