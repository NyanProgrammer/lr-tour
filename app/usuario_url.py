from django.conf.urls import url

from app.usuario_views import * 

urlpatterns = [
    #url(r'^login/$', vistaLogin, name='login'),
    #url(r'^principal/$', vistaPrincipalUsuario, name='principalUsuario'),
    url(r'^registrarse/$', vistaRegistrarse, name='registrarse'),
    url(r'^editarusuario/$', vistaEditarUsuario, name='editarUsuario'),
]