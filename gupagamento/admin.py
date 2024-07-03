from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Contribuinte, Taxa


@admin.register(Contribuinte)
class ContribuinteAdmin(ModelAdmin):
    list_display = ["nome", "morada", "municipio"]
    list_filter = ["municipio"]
    search_fields = ["nome", "nif"]


@admin.register(Taxa)
class TaxaAdmin(ModelAdmin):
    list_display = [
        "titulo",
        "contribuinte",
        "valor_contrato",
        "valor_pago",
        "data_pagamento",
    ]
    search_fields = ["titulo", "contribuinte"]
