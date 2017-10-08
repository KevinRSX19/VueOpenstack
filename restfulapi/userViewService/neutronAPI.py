import json
import urllib3
from django.core.cache import cache


def network_list():
    try:
        token = cache.get("token")
        url = cache.get('url_dic')['neutron']
        if not token:
            return 'session expire'
    except TypeError:
        return 'session expire'
    url += '/v2.0/networks'
    http = urllib3.PoolManager()
    r = http.request(method='GET', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    })
    return r


def subnet_detail(sid):
    try:
        token = cache.get("token")
        url = cache.get('url_dic')['neutron']
        if not token:
            return 'session expire'
    except TypeError:
        return 'session expire'
    url += '/v2.0/subnets' + sid
    http = urllib3.PoolManager()
    r = http.request(method='GET', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    })
    return r
