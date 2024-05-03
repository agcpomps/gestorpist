from django.contrib import admin

from .models import Contribuinte, Licenca


@admin.register(Contribuinte)
class ContribuinteAdmin(admin.ModelAdmin):
    list_display = ["nome", "nif", "morada", "email"]
    search_fields = ["nome", "nif"]


@admin.register(Licenca)
class LicencaAdmin(admin.ModelAdmin):
    list_display = ["numero", "valor", "data_pagamento", "potencia", "distincao"]
    search_fields = ["numero"]
    list_filter = ["data_pagamento", "potencia", "distincao"]
