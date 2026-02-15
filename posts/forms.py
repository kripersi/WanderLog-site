from django import forms
from .models import Post

COUNTRIES = [
    ("Afghanistan", "Afghanistan"),
    ("Albania", "Albania"),
    ("Algeria", "Algeria"),
    ("Argentina", "Argentina"),
    ("Australia", "Australia"),
    ("Austria", "Austria"),
    ("Brazil", "Brazil"),
    ("Canada", "Canada"),
    ("China", "China"),
    ("France", "France"),
    ("Germany", "Germany"),
    ("Italy", "Italy"),
    ("Japan", "Japan"),
    ("Spain", "Spain"),
    ("USA", "USA"),
]


class PostForm(forms.ModelForm):
    country = forms.ChoiceField(
        choices=COUNTRIES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Post
        fields = ["title", "country", "place", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "place": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={
                "rows": 6,
                "class": "form-control"
            }),
        }

    def clean_description(self):
        description = self.cleaned_data["description"]
        if not 100 <= len(description) <= 10000:
            raise forms.ValidationError(
                "Описание должно быть от 100 до 10000 символов"
            )
        return description
