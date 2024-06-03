from django.forms import ModelForm, DateInput

from .models import Empresa, Alvara


class DateInput(DateInput):
    input_type = "date"
    format = ("%d-%m-%Y",)


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
        fields = [
            "numero",
            "emissao",
            "termino",
            "classe",
            "empresa",
            "valor",
            "data_pagamento",
        ]

        widgets = {
            "emissao": DateInput(),
            "termino": DateInput(),
            "data_pagamento": DateInput(),
        }
