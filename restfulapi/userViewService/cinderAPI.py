import urllib3
import json
from django.core.cache import cache


def volume_list():
    try:
        token = cache.get("token")
        url = cache.get('url_dic')['cinderv3']
        pid = cache.get('pid')
        if not token:
            return 'session expire'
    except TypeError:
        return 'session expire'
    url += '/volumes'
    http = urllib3.PoolManager()
    r = http.request(method='GET', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    })
    return json.loads(r.data.decode('utf-8'))


def volume_detail(vid):
    try:
        token = cache.get("token")
        url = cache.get('url_dic')['cinderv3']
        pid = cache.get('pid')
        if not token:
            return 'session expire'
    except TypeError:
        return 'session expire'
    url += '/volumes/' + vid
    http = urllib3.PoolManager()
    r = http.request(method='GET', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    })
    return json.loads(r.data.decode('utf-8'))
