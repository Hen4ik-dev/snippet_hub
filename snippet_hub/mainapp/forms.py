from django import forms
from .models import Snippet

class SnippetCreateForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['title', 'content', 'tags']
        widgets = {
            "title": forms.TextInput(attrs ={
                'class':'form-control',    
            },
            ), 
            "content": forms.Textarea(attrs ={
                'class':'form-control',    
            },
            ), 
            "tags": forms.SelectMultiple(attrs ={
                'class':'form-control',    
            },
            ), 



        }
