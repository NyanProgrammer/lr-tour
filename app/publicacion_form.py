
#Django import
from django import forms
#Django widget
from django.forms import Textarea
from django.forms import TextInput
from django.forms import Select
#Model
from app.models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ('titulo', 'Informacion')
        widgets = {
            'titulo': TextInput(attrs={'class':'form-control'}),
            'Informacion': Textarea(attrs={'class':'form-control','rows':'15'})
        }