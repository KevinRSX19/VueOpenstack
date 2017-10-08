from django.http import HttpResponse
from restfulapi.userViewService import neutronAPI
import json


def get_network_list(request):
    r = neutronAPI.network_list()
    if r == 'session expire':
        return HttpResponse('session expire')
    else:
        return HttpResponse(r.data)

