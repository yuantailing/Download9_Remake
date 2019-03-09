import re
import Download9.view.jsonresponse as JsonResponse
import Download9.view.pageresponse as PageResponse
import Download9.view.database as Database
import Download9.view.control as Control
import Download9.view.aria as Aria
from Download9.view.const import MemoryLimit

def get_overall_state(request):
    if request.is_ajax():
        import json
        if Control.check_session(request):
            usr = Control.get_username_by_session(request)

            x = Database.find_single("account", {"username": usr})
            old = x[Database.id("account", "memoryused")]

            memory = Control.check_memoryuse(request)
            if (memory >= MemoryLimit) and (old < MemoryLimit):
                return JsonResponse.memory_limit_exceeded()

            y = Database.get_all("task", {"username": usr})
            overall_cnt = len(y)
            return JsonResponse.get_overall_state(overall_cnt, memory)

        else:
            return JsonResponse.session_failed()
    else:
        return PageResponse.jump_to_not_exist()

def get_tasks_state(request):
    if request.is_ajax():
        import json
        if Control.check_session(request):
            usr = Control.get_username_by_session(request)

            x = Database.find_single("account", {"username": usr})
            old = x[Database.id("account", "memoryused")]

            memory = Control.check_memoryuse(request)
            if (memory >= MemoryLimit) and (old < MemoryLimit):
                return JsonResponse.memory_limit_exceeded()

            req_all = []
            data = json.loads(request.POST['data'])
            fromurl = request.POST['from']

            needreturn = {}
            for x in data:
                needreturn[x["task_name"]] = x["workid"]

            y = Database.get_all("task", {"username": usr})
            download_cnt = 0
            overall_cnt = len(y)

            for x in y:
                req = Aria.get_task_state(usr, x)
                if (req['state'] == 'active'):
                    download_cnt += 1

                if (re.match(r'^/index/tasks/completed/?$', fromurl)) and (
                        req['state'] == 'complete') and not (
                        needreturn.__contains__(x[Database.id("task", "taskname")])):
                    return JsonResponse.need_refresh()

                if (needreturn.__contains__(x[Database.id("task", "taskname")])):
                    '''print(fromurl)'''
                    if (re.match(r'^/index/tasks/downloading/?$', fromurl)) and (req['state'] != 'active'):
                        return JsonResponse.need_refresh()

                if (needreturn.__contains__(x[Database.id("task", "taskname")])):
                    req['workid'] = needreturn[x[Database.id("task", "taskname")]]
                    if (x[Database.id("task", "attr")] == 0):
                        req['attr'] = "temporary"
                    else:
                        req['attr'] = "persistent"
                    req_all.append(req)

            '''print(req_all)'''
            return JsonResponse.get_tasks_state(req_all, download_cnt, overall_cnt, memory)

        else:
            return JsonResponse.session_failed()
    else:
        return PageResponse.jump_to_not_exist()