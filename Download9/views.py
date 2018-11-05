import json, os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

constjson = open(os.path.join(os.path.dirname(__file__), 'const.json'), 'r', encoding='utf8')
const = json.load(constjson)
hinttitle = const["HINT"]["TITLE"]
hintcontext = const["HINT"]["CONTEXT"]

def login(request):
    print(request.method)
    if (request.method == "POST"):
        try:
            assert request.POST.__contains__("username")
            assert request.POST.__contains__("password")
            return render(request, "template_login.html", {"username": request.POST["username"], "password": request.POST["password"]})
        except:
            return render(request, "template_login.html", {"username": "", "password": ""})
    return render(request, "template_login.html", {"username": "", "password": ""})

def check_login(request):
    if (request.method == "POST"):
        try:
            from Download9.models import account
            from Download9.getmd5 import getmd5
            pwd = getmd5(request.POST["password"])
            x = account.objects.filter(username=request.POST["username"])
            assert x.length == 1
            for i in x:
                assert i.password == pwd
                break
            return HttpResponse("OK")
        except:
            req = {"title": hinttitle["WRONG"], "context": [hintcontext["LOGINWRONG"], hintcontext["JUMPTOINDEX"]],
                   "nexturl": "/index",
                   "FORM": {"username": request.POST["username"], "password": request.POST["password"]}}
            return render(request, "template_jump.html", req)
    else:
        req = {"title": hinttitle["WRONG"], "context": [hintcontext["NEEDLOGIN"], hintcontext["JUMPTOINDEX"]],
               "nexturl": "/index"}
        return render(request, "template_jump.html", req)

def index(request):
    return HttpResponseRedirect("/index")

def not_exist(request):
    req = {"title" : hinttitle["WRONG"] , "context" : [hintcontext["NOTEXIST"], hintcontext["JUMPTOINDEX"]], "nexturl" : "/index"}
    return render(request, "template_jump.html", req)

def jump_to_not_exist(request):
    return HttpResponseRedirect("/not_exist")