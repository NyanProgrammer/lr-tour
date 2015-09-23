#Django Imports 
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.utils import timezone
from datetime import datetime

#Models

from app.models import Comentario_Base
from app.models import Comentario_Publicacion
from app.models import Comentario_Lugar

#forms

from app.comentario_form import comentarioPublicacionForm

def com_edit(request, pk, upk):
    com_v = get_object_or_404(Comentario_Publicacion, pk=pk)
    
    if request.method == "POST":
        form = comentarioPublicacionForm(request.POST, instance = com_v)
        if form.is_valid():
            com = form.save(commit=False)
            com.Fecha_publicacion = datetime.now()
            com.save()
            return redirect('pub_detail', pk = upk)
    else:
        form = comentarioPublicacionForm(instance=com_v)
    return render(
        request,
        'app/comentario_editar.html',
        context_instance = RequestContext(request,
        {
            'title' :'Editar Comentario',
            'year' : datetime.now().year,
            'form': form,
        })
    )