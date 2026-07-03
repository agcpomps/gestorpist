from django.urls import path

from . import views

app_name = "projectos"

urlpatterns = [
    path("", views.project_list, name="list"),
    path("relatorio", views.report, name="report"),
    path("criar", views.project_create, name="create"),
    path("<int:pk>/editar", views.project_edit, name="edit"),
    path("<int:pk>/eliminar", views.project_delete, name="delete"),
]
