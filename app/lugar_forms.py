"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms import Textarea
from django.forms import TextInput
from django.forms import NumberInput
from django.forms import Select

from app.models import Lugar




Regiones = (
    ('I', 'I'),
    ('II', 'III'),
    ('III', 'III'),
    ('IV', 'IV'),
    ('V', 'V'),
    ('VI', 'VI'),
    ('VII', 'VII'),
    ('VIII', 'VIII'),
    ('IX', 'IX'),
    ('X', 'X'),
    ('XI', 'XI'),
    ('XII', 'XII'),
    ('XIII', 'XIII'),
    ('XIV', 'XIV'),
    ('RM', 'RM'),
     )


class LugarForm(forms.ModelForm):

    

    class Meta:
        model = Lugar

        fields = ('nombre','Informacion','Region','Ciudad','Comuna')
        widgets ={
            'nombre': TextInput(attrs={'class':'form-control'}),
            'Informacion': Textarea(attrs={'class':'form-control','rows':'15'}),
            'Region': Select(choices= Regiones,attrs={'class':'form-control' }),
            'Ciudad': TextInput(attrs={'class':'form-control'}),
            'Comuna': TextInput(attrs={'class':'form-control'})
        }