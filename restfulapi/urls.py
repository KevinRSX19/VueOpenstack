from django.conf.urls import include
from django.conf.urls import url

from . import views

app_name = "restfulapi"
urlpatterns = [
    url(r'^network/', include('restfulapi.networks.urls')),
    url(r'^image/', include('restfulapi.images.urls')),
    url(r'^volume/', include('restfulapi.volumes.urls')),
    url(r'^(?P<username>[\w]+)/(?P<password>[\w]+)/$', views.connection, name='connection'),
    url(r'^userlist/$', views.get_user_list, name='getUserList'),
    url(r'^serverlist/$', views.get_server_list, name='getServerList'),
    url(
        r'^create_server/(?P<image>[\w|\W]+)/(?P<flavor>[\w|\W]+)/(?P<network>[\w|\W]+)/(?P<az>[\w|\W]+)/(?P<name>[\w|\W]+)/$',
        views.create_server, name='createServer'),
    url(r'^remove_server/(?P<instance_id>[\w|\W]+)$', views.remove_server, name='removeServer'),
    url(r'^update_server/(?P<name>[\w|\W]+)/(?P<instance_id>[\w|\W]+)$', views.update_server, name='updateServer'),
    url(r'^show_create_instance/$', views.show_create_instance, name='getServerRequire'),
    url(r'^detail/(?P<instance_id>[\w|\W]+)$', views.detail, name='getInstanceDetail'),
    url(r'^actions/$', views.actions, name='instanceActions'),
]
