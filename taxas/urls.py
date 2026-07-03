from django.urls import path


from .views import (
    licenca_list,
    contribuinte_list,
    criar_contribuinte,
    edit_contribuinte,
    delete_contribuinte,
    criar_licenca,
    delete_licenca,
    edit_licenca,
    dashboard,
    arrecadacao_mes_licencas_grafico,
    search,
)

app_name = "taxas"

urlpatterns = [
    path("", licenca_list, name="licenca"),
    path("criar", criar_licenca, name="criarlicenca"),
    path("licenca/<int:pk>/editar", edit_licenca, name="editar_licenca" ),
    path("licenca/<int:pk>", delete_licenca, name="delete_licenca"),
    path("contribuintes/", contribuinte_list, name="contribuintes"),
    path("contribuintes/<int:pk>/editar/", edit_contribuinte, name="editar_contribuinte"),
    path("contribuintes/criar", criar_contribuinte, name="criarcont"),
    path("contribuintes/<int:pk>/", delete_contribuinte, name="delete_contribuinte"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/grafico", arrecadacao_mes_licencas_grafico, name="grafico_licenca_mes"),
    path("search/", search, name="taxas_search"),
]
