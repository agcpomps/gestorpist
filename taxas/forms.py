from django.forms import ModelForm, DateInput 


from .models import Contribuinte, Licenca


class DateInput(DateInput):
    input_type = "date"
    format = ("%d-%m-%Y",)


class ContribuinteForm(ModelForm):
    class Meta:
        model = Contribuinte
        exclude = ["criado_por"] 


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
        
        exclude = ["emitido_por"]

        widgets = {"data_pagamento": DateInput()}
