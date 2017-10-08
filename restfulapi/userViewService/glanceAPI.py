import urllib3
import json
from django.core.cache import cache


# def __init__():
#     try:
#         url = cache.get("url_dic")['glance']
#         if not url:
#             return 'session expire'
#     except KeyError:
#         return 'session expire'


def get_image_name(image_id):
    try:
        token = cache.get("token")
        url = cache.get("url_dic")['glance']
        if not token or not url:
            return 'session expire'
    except TypeError:
        return 'session expire'
    http = urllib3.PoolManager()
    r = http.request(method='GET', url=url + '/v2.0/images/' + image_id, headers={
        'Content-Type': 'application/json', 'X-Auth-Token': token})
    rse = json.loads(r.data.decode('utf-8'))
    return rse['name']


def image_list():
    try:
        token = cache.get("token")
        url = cache.get("url_dic")['glance']
        if not token or not url:
            return 'session expire'
    except TypeError:
        return 'session expire'
    http = urllib3.PoolManager()
    r = http.request(method='GET', url=url + '/v2.0/images', headers={
        'Content-Type': 'application/json', 'X-Auth-Token': token})
    # rse = json.loads(r.data.decode('utf-8'))
    return r


def remove_image(image_id):
    try:
        token = cache.get("token")
        url = cache.get("url_dic")['glance']
        if not token or not url:
            return 'session expire'
    except TypeError:
        return 'session expire'
    http = urllib3.PoolManager()
    r = http.request(method='DELETE', url=url + '/v2.0/images/' + image_id, headers={
        'Content-Type': 'application/json', 'X-Auth-Token': token})
    # rse = json.loads(r.data.decode('utf-8'))
    return r
