from django.urls import path


from .views import (
    licenca_list,
    contribuinte_list,
    criar_contribuinte,
    criar_licenca,
    search,
)

app_name = "taxas"

urlpatterns = [
    path("", licenca_list, name="licenca"),
    path("criar", criar_licenca, name="criarlicenca"),
    path("contribuintes/", contribuinte_list, name="contribuintes"),
    path("contribuintes/criar", criar_contribuinte, name="criarcont"),
    path("search/", search, name="taxas_search"),
]
