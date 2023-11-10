from django.contrib import admin


from .models import Alvara, Empresa, Especialidade

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ["nome", "telefone", "email", "provincia", "municipio"]
    list_filter = ["nome", "provincia", "municipio"]
    search_fields = ["nome", "telefone"]
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ["nome"]
