from Download9.view import const as Const
from Download9.view import database as Database
from Download9.view import aria as Aria

def check_session(Request):
    try:
        assert Request.session.__contains__("MemberName")
        Request.session.set_expiry(Const.Const["Session"]["LoginTime"])
        return True
    except:
        return False

def get_username_by_session(request):
    return request.session["MemberName"]

def check_memoryuse(request):
    usr = get_username_by_session(request)
    from urllib import request
    import re, json
    y = Database.get_all("task", {"username": usr})
    z = []
    memory = 0
    for x in y:
        jsonreq = json.dumps({'jsonrpc': '2.0',
                              'id': usr + str("@") + str(x[Database.id("task", "taskname")]),
                              'method': 'aria2.tellStatus',
                              'params': [x[Database.id("task", "gid")],
                                         ['totalLength',
                                          'completedLength',
                                          'status']]}).encode('utf-8')
        c = json.loads(request.urlopen('http://localhost:6800/jsonrpc', jsonreq).read().decode('utf-8'))
        if (c['result']['status'] == 'active'):
            z.append(x)
        if (re.match('^[1-9][0-9]*$', c['result']['totalLength'])):
            memory += int(c['result']['totalLength'])
        elif (re.match('^[1-9][0-9]*$', c['result']['completedLength'])):
            memory += int(c['result']['completedLength'])
    Database.update("account", {"username": usr}, {"memoryused": memory})

    '''print('checked:', memory)'''
    if memory >= Const.MemoryLimit:
        for x in z:
            jsonreq = json.dumps({'jsonrpc': '2.0',
                                  'id': usr + str("@") + str(x[Database.id("task", "taskname")]),
                                  'method': 'aria2.forcePause',
                                  'params': [x[Database.id("task", "gid")]]}).encode('utf-8')
            request.urlopen('http://localhost:6800/jsonrpc', jsonreq)
    return memory

def auto_delete():
    print('START AUTO DELETE')
    y = Database.get_all("task", {})
    for x in y:
        print(x)
        if (x[Database.id("task", "attr")] == 0):
            try:
                Aria.operate(x[Database.id("task", "username")], x[Database.id("task", "taskname")],
                             x[Database.id("task", "gid")], 'aria2.forcePause')
                Aria.operate(x[Database.id("task", "username")], x[Database.id("task", "taskname")],
                             x[Database.id("task", "gid")], 'aria2.forceRemove')
            except:
                print('NOT ERROR')
            remove_task(x[Database.id("task", "username")], x[Database.id("task", "taskname")], x[Database.id("task", "gid")])

def remove_task(usr, task_name, gid):
    import os
    filedir = Const.DownloadRoot + 'aria2cdownload/' + usr + '/task_' + task_name
    if (os.path.exists(filedir)):
        import shutil
        shutil.rmtree(filedir)
    if (os.path.exists(Const.DownloadRoot + 'aria2cdownload/' + usr + '/task_' + task_name + ".zip")):
        os.remove(Const.DownloadRoot + 'aria2cdownload/' + usr + '/task_' + task_name + ".zip")
    Database.delete("task", {"username": usr, "gid": gid, "taskname": task_name})