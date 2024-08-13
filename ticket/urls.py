from django.urls import path

from .views import list_all_tickets, create_ticket, create_department


app_name = "ticket"

urlpatterns = [
    path("", list_all_tickets, name="ticketall"),
    path("criar", create_ticket, name="create_ticket"),
    path("criar-departamento", create_department, name="create_department"),
]
