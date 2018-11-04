import json, os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

constjson = open(os.path.join(os.path.dirname(__file__), 'const.json'), 'r', encoding='utf8')
const = json.load(constjson)

def login(request):
    return render(request, "template_login.html")

def check_login(request):
    if (request.method == "POST"):
        return HttpResponse("OK")
    else:
        return HttpResponse("NO")

def index(request):
    return HttpResponseRedirect("/index")

def not_exist(request):
    consttitle = const["HINT"]["TITLE"]
    constcontext = const["HINT"]["CONTEXT"]
    req = {"title" : consttitle["WRONG"] , "context" : [constcontext["NOTEXIST"],constcontext["JUMPTOINDEX"]], "nexturl" : "/index"}
    return render(request, "template_jump.html", req)

def jump_to_not_exist(request):
    return HttpResponseRedirect("/not_exist")