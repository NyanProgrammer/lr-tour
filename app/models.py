"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import User , check_password #Normal User ...Useless

#Exceptions
#from django.core.exceptions import ObjectDoesNotExist #Objeto No existe

# Create your models here.

#-------------------->MODULO USUARIOS------------------------------

#Modelo User
#Este modelo viene con el framework , voy a poner sus caracteristicas
#por que le sera util a alguien que lea esto...

#User
    #username(char 30)
    #first_name( char 30 )
    #last_name( char 30 )
    #email (??)
    #password(Mirar en https://docs.djangoproject.com/en/1.8/topics/auth/passwords/)
    #is_staff ( bool )
    #is_active ( bool )
    #is_superuser( bool )
    #last_login ( date )--> (Null by default)
    #date_joined( date )

    #Methods --> https://docs.djangoproject.com/en/1.8/ref/contrib/auth/
    ################

class Usuario_Comun(User): #Esta clase Hereda de Usuario Y modelo
    #Atributos
    #identifier = models.CharField(max_length=40, unique=True)
    #USERNAME_FIELD = 'identifier'

    is_banned = models.BooleanField(default = False) #Si esta Baneado
    informacion = models.CharField(max_length = 200) #Informacion Adicional de Usuario
    tipo = models.CharField(max_length = 50)#Usar Select
    #objects =  UserManager()
    #metodos
    #finMetodos
#Fin de Clase

class Moderador(Usuario_Comun):#Clase Moderador
    #Atributos
    #Permisos(Boolean)
    Eliminar_Comentario = models.BooleanField( default = False ) #Hide or Delete Comment
    Eliminar_Usuarios = models.BooleanField( default = False )   #Hide or delete an User
    Editar_Contenido = models.BooleanField( default = False )    #Editar post Texto remplazar imagenes Etc...
    Baneo = models.BooleanField( default = False )               #Capacidad para banear usuarios
    Habilitar_Lugar = models.BooleanField( default = False )     #Capacidad para Validar que un lugar es correcto y no es falso
    Habilitar_Usuarios = models.BooleanField( default = False )  #Habilitar Usuarios...
    #metodos
    #finMetodos
#Fin de Clase

class FuenteOficial(Usuario_Comun):#Clase Fuente Oficial, puede representar lugares instituciones reporteros Etc..
    #Atributos
    #Nyan::Alert.replace<<Informacion esta repetida Corregir
    Institucion = models.CharField( max_length = 150 ) #Nombre de la institucion
    #metodos
    #finMetodos
#Fin de Clase

#--------------------->MODULO LUGAR----------------------------------------------

class Lugar(models.Model): #Lugar , tambien se puede usar para prototype
    #Atributos
    nombre = models.CharField(max_length = 45)
    Informacion = models.CharField( max_length = 1000 ) #Informacion acerca de el Lugar
    Latitud = models.CharField( max_length = 15 )       #Float To String
    Longitud = models.CharField( max_length = 15 )

    Region = models.CharField(max_length = 45)
    Ciudad = models.CharField(max_length = 45)
    Comuna = models.CharField(max_length = 45)

class Publicacion(models.Model): #Publicacion , se puede usar de prototype
    #Atributos
    titulo = models.CharField(max_length = 200)
    Informacion = models.CharField(max_length = 2000)
    FechaCreacion = models.DateTimeField()#Fecha-->date(yyyy,mm,dd)
    Aprobada = models.BooleanField(default = False)
    Valoraciones = models.IntegerField(default = 0)
    #Cambios al modelo
    FechaPublicacion = models.DateTimeField(blank = True ,null = True)
    #Relaciones
    ID_usuario = models.ForeignKey(User)#Publicaciones estan asociadas a un Usuario
    ID_Lugar = models.ForeignKey(Lugar,blank=True, null=True) #Publicaciones estan asociadas a un Lugar
    #metodos

    def publicar(self):
        self.FechaPublicacion = timezone.now()
        self.save()

    def __str__(self):
        return titulo

    #finMetodos
#Fin de Clase

#--------------------->MODULO COMENTARIOS----------------------------------------


class Comentario_Base(models.Model):#Comentario Base no usar directamente...(Prototype)
    #Atributos
    Fecha_publicacion = models.DateField()      #Fecha-->date(yyyy,mm,dd)
    Respuesta = models.CharField(max_length = 400) #El mensaje
    #Relacion
    ID_usuario = models.ForeignKey(User)        #La relacion es a la clase base-->Inherits from User
    Valoracion = models.IntegerField(default = 0)
    #metodos
    #finMetodos
#Fin de Clase

class Comentario_Lugar(Comentario_Base):#Esta clase expresa una relacion a un Lugar
    #Atributos
    ID_Lugar = models.ForeignKey(Lugar)

    #metodos
    #finMetodos
#Fin de Clase

class Comentario_Publicacion(Comentario_Base):#Esta clase Expresa una relacion a una publicacion...(prototype)
    #Atributos
    ID_Publicacion = models.ForeignKey(Publicacion)

#----------------------------MODULO REPORTES-----------------------------

class Reporte(models.Model):#Clase Base de reporte
    #Atributos
    tipo = models.CharField(max_length = 50)
    Mensaje = models.CharField(max_length = 200)
    Usuario_ID = models.ForeignKey(User)
    #metodos
    #finMetodos
#Fin de Clase

class Reporte_Publicacion(Reporte):#Relacion que indica a que se reporta
    #Atributos
    id_Publicacion = models.ForeignKey( Publicacion )

    #metodos
    #finMetodos
#Fin de Clase

class Reporte_Comentario(Reporte):#Relacion que indica a que se reporta
    #Atributos
    id_Comentario = models.ForeignKey(Comentario_Base)

    #metodos
    #finMetodos
#Fin de Clase

#-----------------------MODULO VALORACION-------------------------------
class Valoracion_Base(models.Model):#Relaciona al usuario que realizo la valoracion
    #Atributos
    UserID = models.ForeignKey(User)
    #metodos
    #finMetodos
#Fin de Clase

class Valoracion_Publicacion(Valoracion_Base):#Realciona a que se hizo una valoracion
    #Atributos
    Publicacion_ID = models.ForeignKey(Publicacion)

    #metodos
    #finMetodos
#Fin de Clase

class Valoracion_Lugar(Valoracion_Base):
    #Atributos
    Lugar_ID = models.ForeignKey(Lugar)

    #metodos
    #finMetodos
#Fin de Clase

class Valoracion_Comentario(Valoracion_Base):
    #Atributos
    Comentario_ID = models.ForeignKey(Comentario_Base)

    #metodos
    #finMetodos
#Fin de Clase

#------------------------MODULO Intereses y Rutas------------------------

class Intereses(models.Model):#Intereses apunta a A un Usuario y Muchos Lugares Equivalente a Favoritos
    #Atributos
    Nombre_Lista = models.CharField(max_length = 20)
    #Usuario al que pertenece esta lista.
    ID_Usuario = models.ForeignKey( User )
    ID_Lugares = models.ManyToManyField(Lugar)#Lista de Lugares -->https://docs.djangoproject.com/en/1.8/topics/db/examples/many_to_many/

    #metodos
    #finMetodos
#Fin de Clase

class Ruta(models.Model):#Una ruta especificada
    nombre = models.CharField(max_length = 45)
    Lugares_ID = models.ManyToManyField(Lugar)
    Usuario_ID = models.ForeignKey(User)
    principio = models.CharField(max_length = 60)
    intermedios = models.CharField(max_length = 10000)
    final = models.CharField(max_length = 60)
