import urllib3
import json
from django.core.cache import cache
from restfulapi.utils import create_server_body, all_combine2json, action_pause, action_unpause


def server_list():
    try:
        token = cache.get("token")
        url = cache.get('url_dic')['nova']
        if not token or not url:
            return 'session expire'
    except TypeError:
        return 'session expire'
    url += '/servers/detail'
    http = urllib3.PoolManager()
    r = http.request(method='GET', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    })
    return r


def server_actions(command, instance_id):
    try:
        token = cache.get("token")
        url = cache.get('url_dic')['nova']
        if not token or not url:
            return 'session expire'
    except TypeError:
        return 'session expire'

    print(command)
    url += '/servers/' + instance_id + '/action'

    if command == "pause":
        values = action_pause()
        r = post_request(token, values, url)
        if r.status is 202:
            return "虚拟机暂停成功"
    elif command == "unpause":
        values = action_unpause()
        r = post_request(token, values, url)
        if r.status is 202:
            return "虚拟机恢复成功"
    else:
        return 'action command error!'

    return r.data


def post_request(token, values, url):
    jdata = json.dumps(values)
    http = urllib3.PoolManager()
    r = http.request(method='POST', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }, body=jdata)
    return r


def create_instance(image, network, flavor, name, az):
    try:
        token = cache.get("token")
        url = cache.get('url_dic')['nova']
        if not token or not url:
            return 'session expire'
    except TypeError:
        return 'session expire'
    url += '/servers'
    values = create_server_body(name, image, flavor, network, az)
    jdata = json.dumps(values)
    print(jdata)
    http = urllib3.PoolManager()
    r = http.request(method='POST', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }, body=jdata)
    return r


def delete_instance(instance_id):
    try:
        token = cache.get("token")
        url = cache.get('url_dic')['nova']
        if not token or not url:
            return 'session expire'
    except TypeError:
        return 'session expire'
    url += '/servers/' + instance_id
    http = urllib3.PoolManager()
    r = http.request(method='DELETE', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    })
    return r


def update_instance(name, instance_id):
    try:
        token = cache.get("token")
        url = cache.get('url_dic')['nova']
        if not token or not url:
            return 'session expire'
    except TypeError:
        return 'session expire'
    url += '/servers/' + instance_id
    values = {
        "server": {
            "name": name
        }
    }
    jdata = json.dumps(values)
    http = urllib3.PoolManager()
    r = http.request(method='PUT', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }, body=jdata)
    return r


def get_imf(token, url):
    http = urllib3.PoolManager()
    r = http.request(method='GET', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    })
    print("searching from: " + url)
    # rse1 = json.loads(r.data.decode('utf-8'))
    # print(str(r.data)[3:-2])
    return str(r.data)[3:-2]


def combine_imf(request):
    try:
        token = cache.get("token")
        url_dic = cache.get('url_dic')
        if not token or not url_dic:
            return 'session expire'
    except TypeError:
        return 'session expire'

    a_zone = get_imf(token, url_dic['nova'] + "/os-availability-zone")
    flavors = get_imf(token, url_dic['nova'] + "/flavors/detail")
    image = get_imf(token, url_dic['glance'] + "/v2.0/images")
    network = get_imf(token, url_dic['neutron'] + "v2.0/networks")
    all_combine = "{" + a_zone + "," + flavors + "," + image + "," + network + "}"
    print(all_combine)
    return all_combine


def server_volumes(server_id):
    try:
        token = cache.get("token")
        url = cache.get('url_dic')['nova']
        if not token or not url:
            return 'session expire'
    except TypeError:
        return 'session expire'
    url += '/servers/'+server_id+'/os-volume_attachments'
    http = urllib3.PoolManager()
    r = http.request(method='GET', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    })
    return r
