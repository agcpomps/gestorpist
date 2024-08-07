from django.contrib import admin
from unfold.admin import ModelAdmin


from .models import Alvara, Empresa, Documento


@admin.register(Empresa)
class EmpresaAdmin(ModelAdmin):
    list_display = [
        "nome",
        "telefone",
        "email",
        "provincia",
        "municipio",
        "especialidade",
    ]
    list_filter = ["nome", "provincia", "municipio", "especialidade"]
    search_fields = ["nome", "telefone"]
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ["nome"]


@admin.register(Alvara)
class AlvaraAdmin(ModelAdmin):
    list_display = [
        "numero",
        "emissao",
        "termino",
        "classe",
        "empresa",
        "valor",
        "data_pagamento",
    ]
    list_filter = [
        "numero",
        "termino",
        "classe",
    ]
    search_fields = ["numero"]
    prepopulated_fields = {"slug": ("numero",)}
    ordering = ["numero"]


@admin.register(Documento)
class DocumentoAdmin(ModelAdmin):
    list_display = ["documento", "descricao"]
    search_fields = ["documento", "descricao"]
