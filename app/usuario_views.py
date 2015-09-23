"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import User
from app.models import Lugar
from django.contrib.auth.forms import UserCreationForm
from app.models import Usuario_Comun
from app.models import Moderador
from app.models import Ruta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def vistaRegistrarse(request):
    if request.method == 'POST':
            userna = request.POST.get('username')
            contra = request.POST.get('password')
            correo = request.POST.get('email')
            nombre = request.POST.get('first_name')
            apellido = request.POST.get('last_name')
            nuevo = Usuario_Comun.objects.create_user(username=userna, password=contra, email=correo, first_name=nombre, last_name=apellido)
            return HttpResponseRedirect('/login')
                
    return render(request,
                  'app/usuario_registro.html',
                  context_instance = RequestContext(
                      request,
                      {
                        'title' : '',
                        'year':datetime.now().year,
                      })
                  )

def vistaEditarUsuario(request):
    if request.method == 'POST':

            #if 'botonLogout' in request.POST:
            #    logout(request)
            #    return HttpResponseRedirect('/')

            usuario_en_cuestion = request.user
            nombre = request.POST.get('username')
            contra = request.POST.get('password')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if (contra != 'Minimo 4 caracteres' and len(contra) >= 4 and contra != usuario_en_cuestion.password):
               request.user.set_password(contra)
               request.user.save()
               print("El usuario ha cambiado su password")

            if (usuario_en_cuestion.username != nombre):
                usuario_en_cuestion.username = nombre
                usuario_en_cuestion.save()
                print("El usuario ha cambiado su username")

            if (usuario_en_cuestion.email != email):
                usuario_en_cuestion.email = email
                usuario_en_cuestion.save()

            if (usuario_en_cuestion.first_name != first_name):
                usuario_en_cuestion.first_name = first_name
                usuario_en_cuestion.save()

                print("El usuario ha cambiado su nombre")

            if (usuario_en_cuestion.last_name != last_name):
                usuario_en_cuestion.last_name = last_name
                usuario_en_cuestion.save()
                print("El usuario ha cambiado su apellido")

            return render(request, 
                          'app/usuario_edit.html', 
                          context_instance = RequestContext(
                              request,
                              {
                                  'usuario': usuario_en_cuestion,
                                  'title' : '',
                                  'year':datetime.now().year,
                              })
                          )

    usuario_definitivo = request.user
    return render(request, 
                  'app/usuario_edit.html', 
                  context_instance = RequestContext(
                      request,
                      {
                          'usuario': usuario_definitivo,
                          'title' : '',
                          'year':datetime.now().year,
                      })
                  )


