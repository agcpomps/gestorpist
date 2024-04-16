from django.contrib import admin

from .models import Contribuinte, Taxa


@admin.register(Contribuinte)
class ContribuinteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'morada', 'municipio']
    list_filter = ['municipio']
    search_fields = ['nome', 'nif']


@admin.register(Taxa)
class TaxaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'contribuinte', 'valor_contrato', 'valor_pago', 'data_pagamento']
    search_fields = ['titulo', 'contribuinte']
