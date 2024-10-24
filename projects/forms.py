from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "start_date", "end_date", "status"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter project title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter project description",
                }
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    start_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "type": "datetime-local",
                "placeholder": "Select start date and time",
            }
        ),
    )
    end_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "type": "datetime-local",
                "placeholder": "Select end date and time",
            }
        ),
    )
