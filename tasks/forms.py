from django import forms

from .models import Category, Task


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Task
        fields = ["title", "description", "category", "priority", "deadline", "is_completed"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class TaskFilterForm(forms.Form):
    query = forms.CharField(required=False, label="Search")
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All categories",
    )
    status = forms.ChoiceField(
        choices=[
            ("all", "All"),
            ("pending", "Pending"),
            ("completed", "Completed"),
        ],
        required=False,
    )
