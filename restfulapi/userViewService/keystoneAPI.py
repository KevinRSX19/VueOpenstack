import json
import urllib3
from restfulapi.utils import login_value
from django.core.cache import cache


def login(username, password):
    url_dic = {}
    url = 'http://10.1.10.105/identity/v3/auth/tokens'
    values = login_value(username, password)
    jdata = json.dumps(values)
    http = urllib3.PoolManager()
    r = http.request(method='POST', url=url, headers={
        'Content-Type': 'application/json'
    }, body=jdata)
    token = r.headers['X-Subject-Token']
    # request.session['token'] = token
    cache.set("token", token, 6000)
    rse = json.loads(r.data.decode('utf-8'))
    print(rse['token']['project']['id'])
    for i in range(0, len(rse['token']['catalog'])):
        url_dic[rse['token']['catalog'][i]['name']] = rse['token']['catalog'][i]['endpoints'][0]['url']
    cache.set('url_dic', url_dic, 6000)
    cache.set('pid', rse['token']['project']['id'])
    return r


def user_list():
    try:
        token = cache.get("token")
        url = cache.get('url_dic')['keystone']
        if not token:
            return 'session expire'
    except TypeError:
        return 'session expire'
    url += '/v3/users'
    http = urllib3.PoolManager()
    r = http.request(method='GET', url=url, headers={
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    })
    return r
