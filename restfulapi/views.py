from django.http import HttpResponse
from restfulapi.userViewService import keystoneAPI, novaAPI, glanceAPI, cinderAPI
import json
import urllib3
from .utils import all_combine2json
from django.core.cache import cache


# login process, with username and password, in to admin field.
def connection(request, username, password):
    r = keystoneAPI.login(username, password)
    rse = json.loads(r.data.decode('utf-8'))
    try:
        print(rse['token']['catalog'])
    except KeyError:
        print(rse['error'])
        return HttpResponse(rse['error']['code'], code=rse['error']['code'])
    return HttpResponse(json.dumps(rse['token']['user']))


# get user list from keystone
def get_user_list(request):
    r = keystoneAPI.user_list()
    if 'session expire' == r:
        return HttpResponse('session expire')
    else:
        return HttpResponse(r.data)


# get server(instance) list from nova, with image and
def get_server_list(request):
    r = novaAPI.server_list()
    if 'session expire' == r:
        return HttpResponse('session expire')
    res = json.loads(r.data.decode('utf-8'))
    for i in range(0, len(res['servers'])):
        if type(res['servers'][i]['image']) == type({}):
            image_id = res['servers'][i]['image']['id']
            image_name = glanceAPI.get_image_name(image_id)
            if image_name == 'session expire':
                return HttpResponse('session expire')
            else:
                res['servers'][i]['image']['name'] = image_name
    res = json.dumps(res)
    # cache.set('server_list', res)
    return HttpResponse(res)


def create_server(request, image, network, flavor, name, az):
    r = novaAPI.create_instance(image, network, flavor, name, az)
    if r == 'session expire':
        return HttpResponse('session expire')
    else:
        return HttpResponse(r.data)


def remove_server(request, instance_id):
    r = novaAPI.delete_instance(instance_id)
    if r == 'session expire':
        return HttpResponse('session expire')
    else:
        return HttpResponse(r.data)


def update_server(request, name, instance_id):
    r = novaAPI.update_instance(name, instance_id)
    if r == 'session expire':
        return HttpResponse('session expire')
    else:
        return HttpResponse(r.data)


def show_create_instance(request):
    a = all_combine2json(novaAPI.combine_imf(request))
    print(a)
    return HttpResponse(a)


def detail(request, instance_id):
    r = novaAPI.server_volumes(instance_id)
    return HttpResponse(r.data)


def actions(request):
    command = request.GET['command']
    instance_id = request.GET['id']
    res = novaAPI.server_actions(command, instance_id)
    return HttpResponse(res)
