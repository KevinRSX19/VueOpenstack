import json


def login_value(username, password):
    values = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": username,
                        "domain": {
                            "name": "Default"
                        },
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "name": "admin",
                    "domain": {
                        "name": "default"
                    }
                }
            }
        }
    }
    return values


def create_server_body(name, image, flavor, network, az):
    values = {
        "server": {
            "name": name,
            "imageRef": image,
            "flavorRef": flavor,
            "networks": [
                {
                    "uuid": network
                }
            ],
            "availability_zone": az
        }
    }
    return values


def all_combine2json(a):
    tot = json.loads(a)
    print(tot)
    # 移除无用image数据
    for i in range(0, len(tot['images'])):
        kicklist = []
        for j in tot['images'][i].keys():
            if j not in ["id", "name", "size", "disk_format", "container_format", "visibility"]:
                kicklist.append(j)
        for k in kicklist:
            tot['images'][i].pop(k)

    # 移除无用flavor数据
    for i in range(0, len(tot['flavors'])):
        kicklist = []
        for j in tot['flavors'][i].keys():
            if j not in ["id", "name", "vcpus", "ram", "disk"]:
                kicklist.append(j)
        for k in kicklist:
            tot['flavors'][i].pop(k)

    # 移除无用network数据
    for i in range(0, len(tot['networks'])):
        kicklist = []
        for j in tot['networks'][i].keys():
            if j not in ["id", "name", "subnets", "shared", "status"]:
                kicklist.append(j)
        for k in kicklist:
            tot['networks'][i].pop(k)

    # 加工成json
    a = str(tot).replace("'", '"')
    a = a.replace("False", "false").replace("True", "true").replace("None", "null")
    return a


def action_pause():
    values = {
        "pause": None
    }
    return values


def action_unpause():
    values = {
        "unpause": None
    }
    return values
