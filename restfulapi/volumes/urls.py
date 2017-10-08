from django.conf.urls import url

from . import views

app_name = 'volumes'
urlpatterns = [
    url(r'^list/$', views.get_volume_list, name='getVolumeList')
]
