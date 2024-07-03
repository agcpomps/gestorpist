from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Contribuinte, Licenca


@admin.register(Contribuinte)
class ContribuinteAdmin(ModelAdmin):
    list_display = ["nome", "nif", "morada", "email"]
    search_fields = ["nome", "nif"]


@admin.register(Licenca)
class LicencaAdmin(ModelAdmin):
    list_display = ["numero", "valor", "data_pagamento", "potencia", "distincao"]
    search_fields = ["numero"]
    list_filter = ["data_pagamento", "potencia", "distincao"]
