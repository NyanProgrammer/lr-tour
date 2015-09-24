﻿"""
Definition of views.
"""

from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponseRedirect

from app.lugar_forms import *

from app.models import Comentario_Base
from app.models import Comentario_Lugar

from app.comentario_form import comentarioLugarForm

def lugar_new(request):
    if request.method == "POST":
        form = LugarForm(request.POST)
        if form.is_valid():
            lug = form.save(commit = False)
            latitud = request.POST['id_Latitud']
            longitud = request.POST['id_Longitud']
            lug.Latitud = latitud
            lug.Longitud = longitud
            lug.save()
            # return HttpResponseRedirect('/lug/ALL/') Arreglar
    else:
        form = LugarForm()

    return render(
        request,
        'app/lugar_edit.html',
        context_instance = RequestContext(request,
        {
            'title' :'Nuevo Lugar',
            'year' : datetime.now().year,
            'form': form,
        })
    )

def lugar_all(request):

    lugs = Lugar.objects.all()
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/lugares_ALL.html',
        context_instance = RequestContext(request,
        {
            'title':'Todos los Lugares',
            'year':datetime.now().year,
            'Lugares': lugs
        })
    )

def lugar_detail(request,pk):
    lug = get_object_or_404(Lugar,pk = pk)
    com = Comentario_Lugar.objects.filter(ID_Lugar = lug)
   #Sentencia de control segura
   #Evita errores de ecritura en BD
    if request.method == "POST":
        form = comentarioLugarForm(request.POST)
        if form.is_valid():
            com_o = form.save(commit = False)
            com_o.ID_Lugar = lug
            com_o.ID_usuario = request.user
            com_o.Fecha_publicacion = datetime.now()
            com_o.save()
            return redirect('lug_detail',pk=lug.pk) 
    else:
        form = comentarioLugarForm()

    return render(
        request,
        'app/lugar_detail.html',
        context_instance = RequestContext(request,
        {
            'title' :lug.nombre,
            'year' : datetime.now().year,
            'lug' : lug,
            'coms' : com,
            'form' :form,
        })
    )

def lug_edit(request, pk):
    lug = get_object_or_404(Lugar, pk=pk)
    
    if request.method == "POST":
        form = LugarForm(request.POST, instance=lug)
        if form.is_valid():
            lug = form.save(commit=False)
            lug.save()
            return redirect('lug_detail', pk=lug.pk)
    else:
        form = LugarForm(instance=lug)
    return render(
        request,
        'app/lugar_edit.html',
        context_instance = RequestContext(request,
        {
            'title' :'Editar lugar',
            'year' : datetime.now().year,
            'form': form,
        })
    )