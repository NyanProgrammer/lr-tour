
#Django Imports 
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.utils import timezone
from datetime import datetime

#Models
from .models import Publicacion
from app.models import User
from app.models import Lugar
from app.models import Comentario_Base
from app.models import Comentario_Publicacion
#custom forms
from app.publicacion_form import *
from app.comentario_form import comentarioPublicacionForm

#Vistas

#Nueva publicacion
def publicacion_detail(request,pk):
    pub = get_object_or_404(Publicacion,pk = pk)
    com = Comentario_Publicacion.objects.filter(ID_Publicacion = pub)
    form  =  comentarioPublicacionForm()

    if request.method == "POST":
        com_o = form.save(commit = False)
        com_o.ID_Publicacion = pub
        com_o.ID_usuario = request.user
        com_o.Fecha_publicacion = datetime.now()
        com_o.save()
        return redirect('pub_detail',pk=pub.pk) 

    elif 'PublicarP' in request.POST:
        pub.publicar()
        pub.save()
    
    

    
    return render(
        request,
        'app/publicacion_detail.html',
        context_instance = RequestContext(request,
        {
            'title' :pub.titulo,
            'year' : datetime.now().year,
            'pub' : pub,
            'form': form,
            'coms' : com,
        })
    )


def pub_new(request):
    lugares = Lugar.objects.all()
    if request.method == "POST":
        form = PublicacionForm(request.POST)
        if form.is_valid():
            idDeRuta = request.POST['opcionLugar']
            lugarElegido = Lugar.objects.get(id=idDeRuta)
            pub = form.save(commit = False)
            pub.ID_Lugar = lugarElegido
            pub.ID_usuario = request.user
            pub.FechaCreacion = timezone.now()
            #pub.publicar()
            pub.save()
            return redirect('pub_detail',pk=pub.pk) 
    else:
        form = PublicacionForm()

    return render(
        request,
        'app/publicacion_edit.html',
        context_instance = RequestContext(request,
        {
            'title' :'Nueva Publicacion',
            'year' : datetime.now().year,
            'form': form,
            'lugares' : lugares
        })
    )

def pub_edit(request, pk):
    pub = get_object_or_404(Publicacion, pk=pk)
    
    if request.method == "POST":
        form = PublicacionForm(request.POST, instance=pub)
        if form.is_valid():
            pub = form.save(commit=False)
            pub.ID_usuario  = request.user
            pub.save()
            return redirect('pub_detail', pk=pub.pk)
    else:
        form = PublicacionForm(instance=pub)
    return render(
        request,
        'app/publicacion_edit.html',
        context_instance = RequestContext(request,
        {
            'title' :'Nueva Publicacion',
            'year' : datetime.now().year,
            'form': form,
        })
    )

def mis_publicaciones(request):
    pubs = Publicacion.objects.filter(ID_usuario = request.user)
    return render(
        request,
        'app/publicaciones_user.html',
        context_instance = RequestContext(request,
        {
            'title' :'Mis Publicaciones',
            'year' : datetime.now().year,
            'pubs': pubs,
        })
    )

def pub_all(request):
    pubs = Publicacion.objects.all()
    return render(
        request,
        'app/publicaciones_user.html',
        context_instance = RequestContext(request,
        {
            'title' :'Mis Publicaciones',
            'year' : datetime.now().year,
            'pubs': pubs,
        })
    )
