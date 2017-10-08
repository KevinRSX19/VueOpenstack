from django.http import HttpResponse
from restfulapi.userViewService import cinderAPI
import json


def get_volume_list(request):
    r = cinderAPI.volume_list()
    if r == 'session expired':
        return HttpResponse('session expired')
    volumes = []
    for a in r['volumes']:
        detail = cinderAPI.volume_detail(a['id'])
        if detail['volume']['name'] == '':
            detail['volume']['name'] = detail['volume']['id']
        detail['volume']['format'] = detail['volume']['volume_image_metadata']['container_format'] + \
                                     '\n/\n' + detail['volume']['volume_image_metadata']['disk_format']
        volumes.append(detail)
    res = json.dumps(volumes)
    return HttpResponse(res)
