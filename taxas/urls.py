from django.urls import path


from .views import licenca_list, contribuinte_list, criar_contribuinte

app_name = "taxas"

urlpatterns = [
    path("", licenca_list, name="licenca"),
    path("contribuintes/", contribuinte_list, name="contribuintes"),
    path("contribuintes/criar", criar_contribuinte, name="criarcont"),
]
