from django.http import HttpResponse
from restfulapi.userViewService import glanceAPI


def get_image_list(request):
    r = glanceAPI.image_list()
    if r == 'session expired':
        return HttpResponse('session expired')
    else:
        return HttpResponse(r.data)


def remove_image(request, image_id):
    r = glanceAPI.remove_image(image_id)
    if r == 'session expired':
        return HttpResponse('session expired')
    else:
        return HttpResponse(r.data)
