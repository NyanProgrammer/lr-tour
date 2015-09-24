#Modelos a utilizar
from app.models import Comentario_Base
from app.models import Comentario_Publicacion
from app.models import Comentario_Lugar

#Forms de Comentarios

from django import forms

#Widgets

from django.forms import Textarea

class comentarioPublicacionForm(forms.ModelForm):

    class Meta:

        model = Comentario_Publicacion
        fields = ('Respuesta',)
        widgets = {
            'Respuesta' : Textarea(attrs = { 'class' : 'form-control input-lg' , 'rows': '2' }),
        }

class comentarioLugarForm(forms.ModelForm):

    class Meta:

        model = Comentario_Lugar
        fields = ('Respuesta',)
        widgets = {
            'Respuesta' : Textarea(attrs = { 'class' : 'form-control input-lg' , 'rows': '2' }),
        }