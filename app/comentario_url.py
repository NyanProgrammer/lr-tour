from django.conf.urls import url
from app.comentario_views import com_edit

urlpatterns = [
    url(r'^com/(?P<pk>[0-9]+)/edit/(?P<upk>[0-9]+)/$', com_edit, name='com_edit')
]