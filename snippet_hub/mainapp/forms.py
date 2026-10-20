from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Snippet


class SnippetCreateForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ["title", "content", "tags", "language"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                },
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                },
            ),
            "tags": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                },
            ),
        }


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1"]
