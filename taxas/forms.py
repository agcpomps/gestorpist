from django.forms import ModelForm


from .models import Contribuinte


class ContribuinteForm(ModelForm):
    class Meta:
        model = Contribuinte
        fields = "__all__"
