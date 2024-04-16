from django.forms import ModelForm

from .models import Empresa, Alvara


class EmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = [
            "nome",
            "gerente",
            "telefone",
            "email",
            "morada",
            "provincia",
            "nif",
            "especialidade",
        ]


class AlvaraForm(ModelForm):
    class Meta:
        model = Alvara
        fields = ["numero", "emissao", "termino", "tipo", "empresa"]
