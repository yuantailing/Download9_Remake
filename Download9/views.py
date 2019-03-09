# Create your views here.

from Download9.view import pageresponse as PageResponse
from Download9.view import jsonresponse as JsonResponse
from Download9.view import account as Account
from Download9.view import const as Const
from Download9.view import aria as Aria
from Download9.view import ajax as Ajax
from Download9.view import control as Control
from Download9.view import database as Database
from Download9.view import operation as Operation

def account9_login(request):
    return PageResponse.jump_to_account9()

def account9_redirect(request):
    return Account.account9_login(request)

def init(request):
    from Download9 import init_database
    return PageResponse.jump_to_index()

def login(request):
    return Account.login(request)

def check_login(request):
    return Account.check_login(request)

def logout(request):
    return Account.logout(request)

def gettaskstate(request):
    return Ajax.get_tasks_state(request)

def getoverallstate(request):
    return Ajax.get_overall_state(request)

def optask(request, method = ""):
    return Operation.optask(request, method)

def downloadtask(request, task_name = "", gid = ""):
    return Operation.download_task(request, task_name, gid)

def jump_to_not_exist(request):
    return PageResponse.jump_to_not_exist()

def taskpage(request, para1 = ""):
    '''print(para1)'''
    if (para1[-1:] == "/"):
        para1 = para1[:-1]
    import re
    usr = Control.get_username_by_session(request)
    y = Database.get_all("task", {"username": usr})
    tasks = []
    TITLE = "全部任务"
    if (re.match(r'^tasks/downloading$', para1)):
        TITLE = "正在下载"
    if (re.match(r'^tasks/completed$', para1)):
        TITLE = "已完成任务"

    for x in y:
        add = True
        if (re.match(r'^tasks/downloading$', para1)):
            req = Aria.get_task_state(usr, x)
            if not(req['state'] == 'active'):
                add = False

        if (re.match(r'^tasks/completed$', para1)):
            req = Aria.get_task_state(usr, x)
            if not(req['state'] == 'complete'):
                add = False

        if (add):
            tasks.append({"taskname": x[Database.id("task", "taskname")],
                          "gid": x[Database.id("task", "gid")],
                          "date": x[Database.id("task", "createtime")]})

    '''print(TITLE)'''
    return PageResponse.task_page(request, usr, TITLE, tasks)

def newpage(request, para1):
    usr = Control.get_username_by_session(request)
    import re
    TITLE = "新建链接任务"
    if (re.match(r'^new/newbt/?$', para1)):
        TITLE = "新建BT任务"
    elif (re.match(r'^new/newmeta/?$', para1)):
        TITLE = "新建磁力任务"
    y = Database.get_all("task", {"username": usr})
    tasks = []
    for i in y:
        tasks.append({"gid": i[Database.id("task", "gid")]})
    return PageResponse.new_task_page(request, usr, TITLE, tasks)

def index(request, para1 = ""):
    '''print(para1)'''
    if Control.check_session(request):
        import re
        if re.match(r'^new(|/(newurl|newbt|newmeta))/?$', para1):
            return newpage(request, para1)
        elif re.match(r'^(|tasks(/(all|downloading|completed))?)/?$', para1):
            return taskpage(request, para1)
        else:
            return PageResponse.jump_to_not_exist()
    else:
        return PageResponse.session_failed(request)

def toindex(request):
    return PageResponse.jump_to_index()

def not_exist(request):
    return PageResponse.page_not_exist(request)

def newtask(request, para1):
    if request.is_ajax():
        if Control.check_session(request):
            usr = Control.get_username_by_session(request)
            y = Database.get_all("task", {"username": usr})

            if (Control.check_memoryuse(request) == -1):
                return JsonResponse.memory_limit_exceeded()

            if len(y) > Const.TaskNumberLimit:
                assert 0
            elif len(y) == Const.TaskNumberLimit:
                return JsonResponse.task_number_exceeded()

            for x in y:
                if (x[Database.id("task", "taskname")] == request.POST["task_name"]):
                    return JsonResponse.task_name_repeated()

            try:
                import base64
                if (para1 == 'bt'):
                    btfile = request.FILES.get("task_link", None)
                    if not btfile:
                        return JsonResponse.upload_btfile_empty()
                    if (btfile.multiple_chunks()):
                        return JsonResponse.upload_btfile_toolarge()
                    else:
                        bt = base64.b64encode(btfile.read()).decode("utf-8")
                        c = Aria.add_other_task(usr, request.POST["task_name"], bt, "aria2.addTorrent")
                elif (para1 == 'meta'):
                    metalink = base64.b64decode(request.POST["task_link"])
                    c = Aria.add_other_task(usr, request.POST["task_name"], metalink, "aria2.addMetalink")
                else:
                    c = Aria.add_url_task(usr, request.POST["task_name"], request.POST["task_link"])
                import time as Time
                Database.insert("task", {"username": usr,
                                         "gid": c["result"],
                                         "taskname": str(request.POST["task_name"]),
                                         "createtime": Time.strftime('%Y-%m-%d', Time.localtime(Time.time())),
                                         "attr": 0})
                return JsonResponse.operation_success()
            except:
                return JsonResponse.download_tool_error()
        else:
            return JsonResponse.session_failed()
    else:
        return PageResponse.jump_to_not_exist()