import django_tables2 as tables
from .models import Licenca


class LicencaHTMxTable(tables.Table):
    class Meta:
        model = Licenca
    
    @classmethod
    def render_paginated_table(cls, request):
        """Render paginated table"""
        table = cls(data=Licenca.objects.all())
        table.paginate(page=request.GET.get("page", 1), per_page=25)
        return table