from django.conf.urls import url
from app.publicacion_views import *

urlpatterns = [
    url(r'^pub/new/$', pub_new, name='pub_new'),
    url(r'^pub/(?P<pk>[0-9]+)/$', publicacion_detail,name ='pub_detail'),
    url(r'^pub/(?P<pk>[0-9]+)/edit/$', pub_edit, name='pub_edit'),
    url(r'^mis/pub$', mis_publicaciones,name ='mis_pub'),
    url(r'^pub/todas/$', pub_all,name ='pub_all')
]