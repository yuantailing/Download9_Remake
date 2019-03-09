import json, re, os
from Download9.view import const as Const
import Download9.view.database as Database
import Download9.view.basic as Basic
from urllib import request

def add_url_task(usr, taskname, url):
    jsonreq = json.dumps({'jsonrpc': '2.0',
                          'id': usr + str("@") + str(taskname),
                          'method': "aria2.addUri",
                          'params': [[url],
                                     {'dir': str(Const.DownloadRoot) + 'aria2cdownload/' + usr + '/task_' + str(taskname)}]}).encode('utf-8')
    return json.loads(request.urlopen('http://localhost:6800/jsonrpc', jsonreq).read().decode('utf-8'))

def add_other_task(usr, taskname, url, method):
    jsonreq = json.dumps({'jsonrpc': '2.0',
                          'id': usr + str("@") + str(taskname),
                          'method': method,
                          'params': [url,
                                     [],
                                     {'dir': str(Const.DownloadRoot) + 'aria2cdownload/' + usr + '/task_' + str(taskname)}]}).encode('utf-8')
    return json.loads(request.urlopen('http://localhost:6800/jsonrpc', jsonreq).read().decode('utf-8'))

def operate(usr, taskname, gid, op):
    JsonReq = json.dumps({'jsonrpc': '2.0',
                          'id': usr + str("@") + str(taskname),
                          'method': op,
                          'params': [gid]}).encode('utf-8')
    request.urlopen('http://localhost:6800/jsonrpc', JsonReq)

def get_filename(usr, taskname, gid):
    JsonReq = json.dumps({'jsonrpc': '2.0',
                          'id': usr + str("@") + str(taskname),
                          'method': 'aria2.getFiles',
                          'params': [gid]}).encode('utf-8')
    a = json.loads(request.urlopen(Const.AriaAddress, JsonReq).read().decode('utf-8'))
    return a['result']

def get_task_state(usr, x):
    req = {}
    try:
        JsonReq = json.dumps({'jsonrpc': '2.0',
                              'id': usr + str("@") + str(x[Database.id("task", "taskname")]),
                              'method': 'aria2.tellStatus',
                              'params': [x[Database.id("task", "gid")],
                                         ['totalLength',
                                          'completedLength',
                                          'status',
                                          'downloadSpeed']]}).encode('utf-8')
        c = json.loads(request.urlopen(Const.AriaAddress, JsonReq).read().decode('utf-8'))

        JsonReq = json.dumps({'jsonrpc': '2.0',
                              'id': usr + str("@") + str(x[Database.id("task", "taskname")]),
                              'method': 'aria2.getFiles',
                              'params': [x[Database.id("task", "gid")]]}).encode('utf-8')
        d = json.loads(request.urlopen(Const.AriaAddress, JsonReq).read().decode('utf-8'))

        filename = os.path.basename(d['result'][0]['path'])
        req['state'] = c['result']['status']
        req['filename'] = filename
        fv = int(c['result']['downloadSpeed'])
        if (req['state'] != 'active'):
            fv = 0
        req['velocity'] = Basic.bytes_to_maxunit(fv) + '/s'
        if (re.match(r'[0-9]+', c['result']['completedLength'])):
            fclen = int(c['result']['completedLength'])
            ftlen = int(c['result']['totalLength'])
            req['process'] = str(int(fclen / ftlen * 100)) + str("%")
            req['size'] = Basic.bytes_to_maxunit(int(c['result']['totalLength']))
            req['timeremain'] = Basic.seconds_to_hms(ftlen - fclen, fv)
        else:
            req['process'] = 'Unknown'
            req['size'] = 'Unknown'
            req['timeremain'] = 'Unknown'
    except:
        req = {'process': "-",
               'state': "error",
               'size': "-",
               'velocity': "-",
               'filename': "-",
               'timeremain': "-"}
    return req