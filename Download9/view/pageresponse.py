from Download9.view.const import HintTitle, HintContext
from Download9.view import const as Const
from django.shortcuts import render, HttpResponseRedirect, render_to_response
from django.http import FileResponse
import os

def jump_to_account9():
    return HttpResponseRedirect("https://accounts.net9.org/api/authorize?client_id=%s&redirect_uri=%s"
                                % (Const.Const["Account9"]["client_id"], Const.Const["ServerRoot"] + "/account9_redirect"))

def jump_to_index():
    return HttpResponseRedirect("/index")

def jump_to_not_exist():
    return HttpResponseRedirect("/not_exist")

def page_not_exist(request):
    req = {"title": HintTitle["Wrong"],
           "context": [HintContext["NotExist"], HintContext["JumpToIndex"]],
           "nexturl": "/index"}
    return render(request, "template_jump.html", req)

def login_success(request):
    req = {"title": HintTitle["Success"],
           "context": [HintContext["JumpToIndex"]],
           "nexturl": "/index"}
    return render(request, "template_jump.html", req)

def login_failed(request, username, password):
    req = {"title": HintTitle["Wrong"],
           "context": [HintContext["LoginWrong"], HintContext["JumpToLogin"]],
           "nexturl": "/login",
           "FORM": {"username": username, "password": password}}
    return render(request, "template_jump.html", req)

def logout(request):
    req = {"title": HintTitle["Success"],
           "context": [HintContext["AlreadyLogout"]],
           "nexturl": "/login"}
    return render(request, "template_jump.html", req)

def not_completed():
    req = {"title": HintTitle["Wrong"],
           "context": [HintContext["NotCompleted"], HintContext["PleaseWait"], HintContext["CloseSoon"]],
           "nexturl": "",
           "close": "1"}
    return render_to_response("template_jump.html", req)

def download_tool_error():
    req = {"result": "fail",
           "title": HintTitle["Wrong"],
           "context": [HintContext["DownloadToolError"], HintContext["Contact"]],
           "nexturl": "/index"}
    return render_to_response("template_jump.html", req)

def session_failed(request):
    print("PAGE:SESSION_FAILED")
    req = {"title": HintTitle["Wrong"],
           "context": [HintContext["NeedLogin"], HintContext["JumpToLogin"]],
           "nexturl": "/login"}
    return render(request, "template_jump.html", req)

def file_download(filedir):
    print(filedir)
    file = open(filedir, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = str('attachment;filename="' + os.path.basename(filedir) + '"')
    return response

def task_page(request, usr, title, tasks):
    req = {"username": usr,
           "tasks": tasks,
           "title": title,
           "tasknumberlimit": Const.TaskNumberLimit,
           "MemoryLimit": Const.MemoryLimit / 1024 / 1024}
    return render(request, "template_task.html", req)

def new_task_page(request, usr, title, tasks):
    req = {"username": usr,
           "tasks": tasks,
           "title": title,
           "tasknumberlimit": Const.TaskNumberLimit,
           "MemoryLimit": Const.MemoryLimit / 1024 / 1024}
    return render(request, "template_newtask.html", req)

def login_page(request, usrename, password):
    return render(request, "template_login.html", {"username": usrename, "password": password})