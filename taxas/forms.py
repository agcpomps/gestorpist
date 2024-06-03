from django.forms import ModelForm, DateInput


from .models import Contribuinte, Licenca


class DateInput(DateInput):
    input_type = "date"
    format = ("%d-%m-%Y",)


class ContribuinteForm(ModelForm):
    class Meta:
        model = Contribuinte
        fields = "__all__"


class LicencaForm(ModelForm):
    class Meta:
        model = Licenca

        fields = [
            "numero",
            "valor",
            "data_pagamento",
            "contribuinte",
            "benificiario",
            "potencia",
            "distincao",
        ]

        widgets = {"data_pagamento": DateInput()}
