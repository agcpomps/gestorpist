from django import forms

from .models import Project


class DateInput(forms.DateInput):
    input_type = "date"


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Non-staff users only create/edit projects in their own department.
        if user is not None and not user.is_staff:
            department_field = self.fields["department"]
            department_field.queryset = department_field.queryset.filter(
                pk=user.departamento_id
            )
            department_field.initial = user.departamento_id

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "department",
            "status",
            "priority",
            "manager",
            "members",
            "start_date",
            "end_date",
        ]
        widgets = {
            "start_date": DateInput(),
            "end_date": DateInput(),
        }
