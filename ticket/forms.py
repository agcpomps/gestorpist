from django import forms

from accounts.models import Department

from .models import Ticket, TicketComment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "priority", "department", "assigned_to"]


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["status", "priority", "assigned_to"]


class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "placeholder": "Escreva um comentário..."}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "description"]
