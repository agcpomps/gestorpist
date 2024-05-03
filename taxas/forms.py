from django.forms import ModelForm


from .models import Contribuinte, Licenca


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
