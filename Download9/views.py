import json, os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

constjson = open(os.path.join(os.path.dirname(__file__), 'const.json'), 'r', encoding='utf8')
const = json.load(constjson)
hinttitle = const["HINT"]["TITLE"]
hintcontext = const["HINT"]["CONTEXT"]

def gettaskstate(request):
    if request.is_ajax():
        import json
        if check_session(request):
            usr = GETusernameBYsession(request);
            try:
                REQUEST = request
                from urllib import request
                from Download9.models import task
                import re
                jsonreq = json.dumps({'jsonrpc': '2.0',
                                      'id': usr + str("@") + str(REQUEST.POST["task_name"]),
                                      'method': 'aria2.tellStatus',
                                      'params': [REQUEST.POST["gid"],
                                                 ['totalLength',
                                                  'completedLength',
                                                  'status',
                                                  'downloadSpeed']]}).encode('utf-8')
                c = json.loads(request.urlopen('http://localhost:6800/jsonrpc', jsonreq).read().decode('utf-8'))
                jsonreq = json.dumps({'jsonrpc': '2.0',
                                      'id': usr + str("@") + str(REQUEST.POST["task_name"]),
                                      'method': 'aria2.getFiles',
                                      'params': [REQUEST.POST["gid"]]}).encode('utf-8')
                d = json.loads(request.urlopen('http://localhost:6800/jsonrpc', jsonreq).read().decode('utf-8'))
                filename = os.path.basename(d['result'][0]['path']);
                req = {'result': 'success',
                       'workid': str(REQUEST.POST['workid']),
                       'state': c['result']['status'],
                       'size': c['result']['totalLength'],
                       'velocity': c['result']['downloadSpeed'],
                       'filename': filename}
                return HttpResponse(json.dumps(req))
            except:
                return HttpResponse(json.dumps({'result': 'fail'}))
        else:
            return HttpResponse(json.dumps({'result': 'session_failed'}))
    else:
        return not_exist(request)

def logout(request):
    request.session.flush()
    req = {"title": hinttitle["SUCCESS"], "context": [hintcontext["ALREADYLOGOUT"]],
           "nexturl": "/login"}
    return render(request, "template_jump.html", req)

def taskpage(request):
    from Download9.models import task
    x = GETusernameBYsession(request)
    y = task.objects.filter(username=x)
    tasks = []
    for i in y:
        tasks.append({"taskname": i.taskname, "gid": i.gid})
    req = {"username": x, "tasks": tasks}
    return render(request, "template_task.html", req);

def newpage(request):
    from Download9.models import task
    x = GETusernameBYsession(request)
    y = task.objects.filter(username=x)
    tasks = []
    for i in y:
        tasks.append({"gid": i.gid})
    req = {"username": x, "tasks": tasks}
    return render(request, "template_newtask.html", req);

def login(request):
    if check_session(request):
        return HttpResponseRedirect("/index")
    if (request.method == "POST"):
        try:
            assert request.POST.__contains__("username")
            assert request.POST.__contains__("password")
            return render(request, "template_login.html", {"username": request.POST["username"], "password": request.POST["password"]})
        except:
            return render(request, "template_login.html", {"username": "", "password": ""})
    return render(request, "template_login.html", {"username": "", "password": ""})

def check_session(request):
    try:
        assert request.session.__contains__("memberid")
        request.session.set_expiry(const["SESSION"]["LOGINTIME"])
        return True
    except:
        return False

def GETusernameBYsession(request):
    from Download9.models import account
    return account.objects.get(id=request.session["memberid"]).username

def check_login(request):
    if (request.method == "POST"):
        try:
            from Download9.models import account
            from Download9.getmd5 import getmd5
            pwd = getmd5(request.POST["password"])
            x = account.objects.get(username=request.POST["username"])
            assert x.password == pwd
            request.session["memberid"] = x.id
            request.session.set_expiry(const["SESSION"]["LOGINTIME"])
            return HttpResponseRedirect("/index")
        except:
            req = {"title": hinttitle["WRONG"], "context": [hintcontext["LOGINWRONG"], hintcontext["JUMPTOLOGIN"]],
                   "nexturl": "/login",
                   "FORM": {"username": request.POST["username"], "password": request.POST["password"]}}
            return render(request, "template_jump.html", req)
    else:
        return index(request)

def index(request, para1 = ""):
    print(para1)
    if check_session(request):
        import re
        if re.match(r'^new', para1):
            return newpage(request)
        else:
            return taskpage(request)
    else:
        req = {"title": hinttitle["WRONG"], "context": [hintcontext["NEEDLOGIN"], hintcontext["JUMPTOLOGIN"]],
               "nexturl": "/login"}
        return render(request, "template_jump.html", req)

def toindex(request):
    return HttpResponseRedirect("/index")

def not_exist(request):
    req = {"title": hinttitle["WRONG"], "context": [hintcontext["NOTEXIST"], hintcontext["JUMPTOINDEX"]],
           "nexturl": "/index"}
    return render(request, "template_jump.html", req)

def jump_to_not_exist(request):
    return HttpResponseRedirect("/not_exist")

def newurltask(request):
    print("newurltest")
    if request.is_ajax():
        import json
        if check_session(request):
            usr = GETusernameBYsession(request);
            print("output1")
            try:
                REQUEST = request
                from urllib import request
                from Download9.models import task
                jsonreq = json.dumps({'jsonrpc': '2.0',
                                      'id': usr+str("@")+str(REQUEST.POST["task_name"]),
                                      'method': 'aria2.addUri',
                                      'params': [[REQUEST.POST["task_link"]]]}).encode('utf-8')
                c = json.loads(request.urlopen('http://localhost:6800/jsonrpc', jsonreq).read().decode('utf-8'))
                task.objects.create(username=usr, gid=c['result'], taskname=str(REQUEST.POST["task_name"]))
                return HttpResponse(json.dumps({"result": "success"}))
            except:
                return HttpResponse(json.dumps({"result": "fail"}))
        else:
            print("output2")
            return HttpResponse(json.dumps({"result": "session_failed"}))
    else:
        print("output3")
        return not_exist(request)