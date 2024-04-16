from django.contrib import admin


from .models import Alvara, Empresa, Documento


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
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
class AlvaraAdmin(admin.ModelAdmin):
    list_display = ["numero", "emissao", "termino", "tipo", "empresa"]
    list_filter = ["numero", "termino", "tipo"]
    search_fields = ["numero"]
    prepopulated_fields = {"slug": ("numero",)}
    ordering = ["numero"]


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ["documento", "descricao"]
    search_fields = ["documento", "descricao"]
