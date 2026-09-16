from django import forms
from main.models import Education, Project


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ["institution", "degree", "start_year", "end_year"]

        labels = {
            "institution": "Institution",
            "degree": "Degree",
            "start_year": "Start Year",
            "end_year": "End Year",
        }

        widgets = {
            "institution": forms.TextInput(attrs={
                "placeholder": "e.g. Universitas Indonesia",
            }),
            "degree": forms.TextInput(attrs={
                "placeholder": "e.g. S1 Ilmu Komputer",
            }),
            "start_year": forms.NumberInput(attrs={
                "placeholder": "e.g. 2025",
            }),
            "end_year": forms.NumberInput(attrs={
                "placeholder": "e.g. 2029",
            }),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Project Title",
            "description": "Description",
            "tech_stack": "Tech Stack",
            "project_url": "Project URL",
            "project_image_url": "Project Image URL",
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "e.g. Personal Portfolio Website",
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Describe your project...",
                "rows": 5,
            }),
            "tech_stack": forms.TextInput(attrs={
                "placeholder": "e.g. HTML, CSS, Django",
            }),
            "project_url": forms.URLInput(attrs={
                "placeholder": "https://github.com/...",
            }),
            "project_image_url": forms.URLInput(attrs={
                "placeholder": "https://...",
            }),
        }