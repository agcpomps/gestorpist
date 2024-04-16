from django import forms


from .models import Taxa, Contribuinte


class DateInput(forms.DateInput):
    input_type = "date"


class TaxaForm(forms.ModelForm):
    class Meta:
        model = Taxa
        fields = (
            "contribuinte",
            "titulo",
            "valor_contrato",
            "valor_pago",
            "data_pagamento",
        )
        widgets = {
            "data_pagamento": DateInput(),
        }


class ContribuinteForm(forms.ModelForm):
    class Meta:
        model = Contribuinte
        fields = "__all__"