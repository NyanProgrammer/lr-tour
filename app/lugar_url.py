from django.conf.urls import url

from app.lugar_views import * 

urlpatterns = [
    url(r'^lug/new/$', lugar_new, name='lug_new'),
    url(r'^lug/ALL/$', lugar_all, name='lug_all'),
    url(r'^lug/(?P<pk>[0-9]+)/$', lugar_detail,name ='lug_detail'),
    url(r'^lug/(?P<pk>[0-9]+)/edit/$', lug_edit, name='lug_edit')
]