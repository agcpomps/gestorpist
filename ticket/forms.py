from django import forms


from .models import Ticket, Department


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "priority", "department", "assigned_to"]


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "description"]
