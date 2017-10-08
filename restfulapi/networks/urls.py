from django.conf.urls import url

from . import views

app_name = 'networks'
urlpatterns = [
    url(r'^list/$', views.get_network_list, name='getNetworkList')
]
