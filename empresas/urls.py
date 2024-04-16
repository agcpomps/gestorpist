from django.urls import path

from .views import empresas, alvara, criar_empresa, criar_alvara, search_empresa

app_name = "empresas"


urlpatterns = [
    path("", empresas, name="empresas"),
    path("alvaras/", alvara, name="alvaras"),
    path("criar/", criar_empresa, name="criar"),
    path("alvaras/criar/", criar_alvara, name="alvaracriar"),
    path("search/", search_empresa, name="search_empresa"),
]
