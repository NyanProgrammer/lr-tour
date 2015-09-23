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

# Corresponde a la vista con url: /rutas/nuevaruta/, a esta vista se llega al haber seleccionado en la vista "vistaRutasUsuario"
# la opcion de "Crear nueva Ruta", y tal como lo dice la opcion, esta vista se encarga de todo el proceso de generado y guardado
# de una nueva ruta.
def vistaRutas(request):

    # Si el usuario desea guardar ruta.
    if 'guardarRuta' in request.POST:
            
            # Se asigna a esta variable la instancia del modelo User del usuario que se encuentra actualmente logeado.
            usuarioActual = request.user
            # Se recoge el string que el usuario eligio como nombre de ruta.
            nombreRuta = request.POST['nombreRuta']
            # Se recoge el string del orden de la ruta del usuario.
            stringDeRuta = request.POST['guardarRuta']
            # Se separan el string en una lista de elementos.
            lugaresDeLaRuta = stringDeRuta.split('/')
            # Se obtiene la posicion del lista, en donde se encuentra el string cuyo valor es la cantidad de puntos intermedios
            # que existen en la ruta a almacenar.
            posicionDeLaCantidadDePuntosInter = len(lugaresDeLaRuta)
            # Se obtienen las coordenadas y el nombre del lugar que representa el comienzo de la ruta.
            comienzo = lugaresDeLaRuta[0].split(',')
            # Se utiliza el id del lugar, para buscar en el modelo Lugar, el objeto determinado
            # que representa el comienzo de la ruta.
            principioDeLaRuta = Lugar.objects.get(id=(comienzo[3]))
            # Se asigna a esta variable el nombre del lugar que es el comienzo de la nueva ruta.
            principioDeLaNuevaRuta = (principioDeLaRuta.nombre)
            # Se obtiene la cantidad de puntos intermedios que existen en la ruta a guardar, variable que se almaceno y conto en
            # en el Javascript de "ruta.html".
            cantidadDePuntosInter = int(lugaresDeLaRuta[posicionDeLaCantidadDePuntosInter - 1])
            # Se inicializa la variable.
            intermediosDeLaNuevaRuta = ""
            # Ciclo for in en donde se van obtiendo los elementos especificos de modelo Lugar, que corresponden a puntos intermedios en la ruta
            # y ademas se configura un string que almacena el orden de estos puntos intermedios.
            for i in range(int(cantidadDePuntosInter)):

                if (i == 0):

                   puntoIntermedio = lugaresDeLaRuta[i+2].split(',')
                   puntoIntermedioDeLaRuta = Lugar.objects.get(id=(puntoIntermedio[3]))
                   intermediosDeLaNuevaRuta = puntoIntermedioDeLaRuta.nombre

                elif (i != 0):

                   puntoIntermedio = lugaresDeLaRuta[i+2].split(',')
                   puntoIntermedioDeLaRuta = Lugar.objects.get(id=(puntoIntermedio[3]))
                   intermediosDeLaNuevaRuta += '/' + puntoIntermedioDeLaRuta.nombre

            # Se obtiene el string que almacena las coordenadas y el nombre del lugar que representa el final de la ruta.
            final = lugaresDeLaRuta[1].split(',')
            # Se utiliza el id del lugar, para buscar en el modelo Lugar, el objeto determinado
            # que representa el comienzo de la ruta.
            finalDeLaRuta = Lugar.objects.get(id=(final[3]))
            # Se asigna a esta variable el nombre del lugar que es el final de la nueva ruta.
            finalDeLaNuevaRuta = finalDeLaRuta.nombre
            # Se crea el elemento Ruta con los lugares elegidos por el usuario.
            nuevaRuta = Ruta(nombre=nombreRuta, Usuario_ID=usuarioActual, principio=principioDeLaNuevaRuta, final=finalDeLaNuevaRuta, intermedios=intermediosDeLaNuevaRuta)
            # Se guarda el nuevo elemento ruta.
            nuevaRuta.save()
            # Se agrega el Lugar que representa el comienzo de la ruta a la relacion de ManytoMany.
            nuevaRuta.Lugares_ID.add(principioDeLaRuta)
            # Se agregan los Lugares que representan los puntos intermedios de la ruta a la relacion de ManytoMany.
            for i in range(int(cantidadDePuntosInter)):

                 puntoIntermedio = lugaresDeLaRuta[i+2].split(',')
                 puntoIntermedioDeLaRuta = Lugar.objects.get(id=(puntoIntermedio[3]))
                 nuevaRuta.Lugares_ID.add(puntoIntermedioDeLaRuta)

            # Se agrega el Lugar que representa el final de la ruta a la relacion de ManytoMany.
            nuevaRuta.Lugares_ID.add(finalDeLaRuta)
            # Una vez creada la ruta se devuelve la vista donde se presentan todas las rutas del usuario.
            return HttpResponseRedirect('/rutas/misrutas')
    
    # El ingreso a la vista comienza en este punto, donde se cargan todos los modelo Lugar, que como lo dice su nombre corresponden
    # a todos los lugares disponibles que el usuario puede elegir para visitar.
    todosLosLugaresDisponibles = Lugar.objects.all()

    # Se manda a cargar el render de ruta.html, donde se nos presentara la interfaz necesaria para configurar nuestra nueva ruta
    # a nuestro gusto.
    return render(request, 
                  'app/ruta.html', 
                  context_instance = RequestContext(
                      request,
                      {
                          #'title':'',
                          'lugares' : todosLosLugaresDisponibles,
                          #'year':datetime.now().year,
                      })
                  )

# Corresponde a la vista con url: /rutas/, a esta vista se llega al haber seleccionado la opcion de "Mis Rutas"
# en el menu principal de usuario.
def vistaRutasUsuario(request):
    if 'botonDeEliminacionDeRuta' in request.POST:
        idDeRuta = request.POST['botonDeEliminacionDeRuta']
        rutaAEliminar = Ruta.objects.get(id=int(idDeRuta))
        rutaAEliminar.Lugares_ID.clear()
        # Se elimina la ruta.
        rutaAEliminar.delete()
        return HttpResponseRedirect('/rutas/misrutas')
    # Corresponde a la opcion de editar una ruta previamente creada.
    elif 'botonDeEdicionDeRuta' in request.POST:
            # Se asigna a esta variable la instancia del modelo User del usuario que se encuentra actualmente logeado.
            usuarioActual = request.user
            # Se obtiene el id de la ruta seleccionada de html.
            idDeRuta = request.POST['botonDeEdicionDeRuta']
            # Se crea una lista vacia.
            listaDeLugaresDeLaRuta = []
            # Se obtiene la ruta a editar del modelo Ruta.
            rutaAEditar = Ruta.objects.get(id=int(idDeRuta))
            # Se obtienen los lugares de la ruta, haciendo una busqueda primero del id y luego obtiendo lo lugares que la componen.
            listaDeLugaresDeLaRuta = Lugar.objects.filter(ruta__id=idDeRuta)
            # Se almacena en una variable la lista de todos los lugares.
            listaDeLugaresGenerales = Lugar.objects.all()
            # Se almacena en una variable el largo de la ruta.
            largoDeLaRuta = len(listaDeLugaresDeLaRuta)
            # Se almacena en una variable el nombre de la ruta.
            nombreDeLaRuta = rutaAEditar.nombre
            # Se obtiene el comienzo de la ruta, del modelo Lugar.
            primerLugarDeLaRuta = Lugar.objects.get(nombre=(rutaAEditar.principio))
            # Se obtiene el final de la ruta, del modelo Lugar.
            ultimoLugarDeLaRuta = Lugar.objects.get(nombre=(rutaAEditar.final))
            # Se obtienen los nombres de los lugares intermedios de la ruta.
            intermedios = (rutaAEditar.intermedios).split('/')
            # Se crea una lista vacia.
            listaDeIntermedios = []
            # Ese ciclo se inicializa solo si la ruta a editar posee lugares intermedios.
            if(intermedios[0] != ""):
               # Por cada lugar intermedio que exista en la ruta.
               for intermedio in intermedios:
                   # Se busca por nombre el lugar en el modelo Lugar.
                   intermedioDeLaRuta = Lugar.objects.get(nombre=intermedio)
                   # El lugar encontrado se agrega a la lista vacia.
                   listaDeIntermedios.append(intermedioDeLaRuta)
            # Se manda a cargar el render de ruta_editar.html, donde se nos presentara la interfaz necesaria para editar la ruta seleccionada
            return render(request,
                          'app/ruta_editar.html',
                          {
                                  'lugaresDeLaRuta': listaDeLugaresDeLaRuta , 
                                  'lugares' : listaDeLugaresGenerales, 
                                  'largoDeLaRuta' : largoDeLaRuta, 
                                  'idDeRuta' : idDeRuta, 
                                  'primerLugarDeLaRuta' : primerLugarDeLaRuta , 
                                  'ultimoLugarDeLaRuta' : ultimoLugarDeLaRuta, 
                                  'listaDeIntermedios' : listaDeIntermedios, 
                                  'nombreDeLaRuta' : nombreDeLaRuta
                                  #'year':datetime.now().year,
                                  #'title':'',
                               })
                          
    # Corresponde a la opcion de guardar la ruta una vez editada, a esta opcion solo se puede acceder si se accedio al render de "ruta_editar.html"
    elif 'guardarRuta' in request.POST:
            # Se asigna a esta variable la instancia del modelo User del usuario que se encuentra actualmente logeado.
            usuarioActual = request.user
            # Se recoge el string que el usuario eligio como nombre de ruta.
            nombreRuta = request.POST['nombreRuta']
            # Se recoge el string del orden de la ruta del usuario.
            stringDeRuta = request.POST['guardarRuta']
            # Se separan el string en una lista de elementos.
            lugaresDeLaRuta = stringDeRuta.split('/')
            # Se obtiene la ruta a editar del Modelo Ruta a partir del id.
            RutaAModificar = Ruta.objects.get(id=int(lugaresDeLaRuta[0].strip()))
            # Se eliminan las relaciones antiguas de la ruta a modificar.
            RutaAModificar.Lugares_ID.clear()
            # Se elimina la ruta.
            RutaAModificar.delete()
            # Se obtiene la posicion del lista, en donde se encuentra el string cuyo valor es la cantidad de puntos intermedios
            # que existen en la ruta a almacenar.
            posicionDeLaCantidadDePuntosInter = len(lugaresDeLaRuta)
            # Se obtienen las coordenadas y el nombre del lugar que representa el comienzo de la ruta.
            comienzo = lugaresDeLaRuta[1].split(',')
            # Se utiliza el id del lugar, para buscar en el modelo Lugar, el objeto determinado que representa el comienzo de la ruta.
            principioDeLaRuta = Lugar.objects.get(id=(comienzo[3]))
            # Se asigna a esta variable el nombre del lugar que es el comienzo de la nueva ruta.
            principioDeLaNuevaRuta = (principioDeLaRuta.nombre)
             # Se obtiene la cantidad de puntos intermedios que existen en la nueva configuracion de ruta, variable que anteriormente se almaceno y conto en
            # en el Javascript de "ruta_editar.html".
            cantidadDePuntosInter = int(lugaresDeLaRuta[posicionDeLaCantidadDePuntosInter - 1])
            # Se inicializa esta variable.
            intermediosDeLaNuevaRuta = ""
            # Ciclo for in en donde se van obtiendo los elementos especificos de modelo Lugar, que corresponden a puntos intermedios en la ruta
            # y ademas se configura un string que almacena los nombres puntos intermedios en orden.
            for i in range(int(cantidadDePuntosInter)):

                if (i == 0):

                   puntoIntermedio = lugaresDeLaRuta[i+3].split(',')
                   puntoIntermedioDeLaRuta = Lugar.objects.get(id=(puntoIntermedio[3]))
                   intermediosDeLaNuevaRuta = puntoIntermedioDeLaRuta.nombre

                elif (i != 0):

                   puntoIntermedio = lugaresDeLaRuta[i+3].split(',')
                   puntoIntermedioDeLaRuta = Lugar.objects.get(id=(puntoIntermedio[3]))
                   intermediosDeLaNuevaRuta += '/' + puntoIntermedioDeLaRuta.nombre
            # Se obtiene el string que almacena las coordenadas y el nombre del lugar que representa el final de la ruta.
            final = lugaresDeLaRuta[2].split(',')
            # Se utiliza el id para buscar en el modelo Lugar, el objeto determinado que representa el comienzo de la ruta.
            finalDeLaRuta = Lugar.objects.get(id=(final[3]))
            # Se asigna a esta variable el nombre del lugar que es el final de la nueva ruta.
            finalDeLaNuevaRuta = finalDeLaRuta.nombre
            # Se crea la nueva ruta que contendra las nuevas configuracion otorgadas por el usuario.
            nuevaRuta = Ruta(nombre=nombreRuta, Usuario_ID=usuarioActual, principio=principioDeLaNuevaRuta, final=finalDeLaNuevaRuta, intermedios=intermediosDeLaNuevaRuta)
            # Se guarda la nueva ruta.
            nuevaRuta.save()
            # Se agrega el Lugar que representa el comienzo de la ruta a la relacion de ManytoMany.
            nuevaRuta.Lugares_ID.add(principioDeLaRuta)
            # Se agregan los Lugares que representan los puntos intermedios de la ruta a la relacion de ManytoMany.
            for i in range(int(cantidadDePuntosInter)):

                 puntoIntermedio = lugaresDeLaRuta[i+3].split(',')
                 puntoIntermedioDeLaRuta = Lugar.objects.get(id=(puntoIntermedio[3]))
                 nuevaRuta.Lugares_ID.add(puntoIntermedioDeLaRuta)
            # Se agrega el Lugar que representa el final de la ruta a la relacion de ManytoMany.
            nuevaRuta.Lugares_ID.add(finalDeLaRuta)
            # Una vez configurada la ruta se devuelve a la vista donde se presentan todas las rutas del usuario.
            return HttpResponseRedirect('/rutas/misrutas')
    # Si se elige la opcion de crear nueva ruta, se nos envia a la vista "vistaRutasUsuario".
    elif 'botonDeNuevaRuta' in request.POST:
        return HttpResponseRedirect('/rutas/nuevaruta')

    # Se asigna a esta variable la instancia del modelo User del usuario que se encuentra actualmente logeado.
    usuarioActual = request.user
    # Se obtiene la lista de rutas del usuario.
    listaDeRutasDelUsuario = Ruta.objects.filter(Usuario_ID__id=usuarioActual.id)
    # Se manda a cargar el render de ruta_usr.html, donde se nos presentaran la rutas pertenecientes al usuario actualmente logeado,
    # y dandole las opciones para crear una nueva ruta, y borrar o editar una ruta ya creada.
    return render(request, 
                  'app/rutas_usr.html', 
                  context_instance = RequestContext(
                      request,
                      {
                          'ListaDeRutas' : listaDeRutasDelUsuario,
                          'year':datetime.now().year,
                          'title':'',
                      })
                  )