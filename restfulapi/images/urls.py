from django.conf.urls import url

from . import views

app_name = 'images'
urlpatterns = [
    url(r'^list/$', views.get_image_list, name='getImageList'),
    url(r'^remove_image/(?P<image_id>[*]+)/$', views.remove_image, name='removeImage')
]
