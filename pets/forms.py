
from django import forms
from .models import Pet_Model

class PostForm(forms.ModelForm):
    class Meta:
        model = Pet_Model
        fields = '__all__'