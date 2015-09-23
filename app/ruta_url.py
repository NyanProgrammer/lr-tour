from django.conf.urls import url

from app.ruta_views import * 

urlpatterns = [
    url(r'^misrutas/$', vistaRutasUsuario, name='misrutas'),
    url(r'^nuevaruta/$', vistaRutas, name='nuevaruta')
]