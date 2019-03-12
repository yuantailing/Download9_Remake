import os
import Download9.view.jsonresponse as JsonResponse
import Download9.view.pageresponse as PageResponse
import Download9.view.database as Database
import Download9.view.control as Control
import Download9.view.const as Const
import Download9.view.aria as Aria

def optask(request, method):
    import json
    if request.is_ajax():
        if Control.check_session(request):
            print(method)
            op = []
            if (method == 'delete'):
                op = ['aria2.forcePause', 'aria2.forceRemove']
            elif (method == 'pause'):
                op = ['aria2.forcePause']
            elif (method == 'continue'):
                if (Control.check_memoryuse(request) >= Const.MemoryLimit):
                    return JsonResponse.memory_limit_exceeded()
                else:
                    op = ['aria2.unpause']
            elif (method == 'switch'):
                op = []
            usr = Control.get_username_by_session(request)

            y = json.loads(request.POST['jsonData'])
            for x in y:
                for xop in op:
                    try:
                        Aria.operate(usr, x["task_name"], x["gid"], xop)
                    except:
                        print('NOT ERROR')

                if (method == 'delete'):
                    Control.remove_task(usr, x["task_name"], x["gid"])

                if (method == 'switch'):
                    thisone = Database.find_single("task", {"username": usr, "gid": x["gid"], "taskname": x["task_name"]})
                    Database.update("task", {"username": usr, "gid": x["gid"], "taskname": x["task_name"]}, {"attr": 1 - thisone[Database.id("task", "attr")]})

            return JsonResponse.operation_success()
        else:
            return JsonResponse.session_failed()
    else:
        return PageResponse.jump_to_not_exist()

def download_task(request, task_name, gid):
    '''print(task_name)
    print(gid)'''
    if Control.check_session(request):
        usr = Control.get_username_by_session(request)
        try:
            y = Database.find_single("task", {"username": usr, "taskname": task_name, "gid": gid})

            req = Aria.get_task_state(usr, y)

            if (req['state'] != 'complete'):
                return PageResponse.not_completed()

            filedir = Aria.get_filename(usr, task_name, gid)
            if (len(filedir) == 1):
                return PageResponse.file_download(filedir[0]["path"])
            else:
                dirname = Const.DownloadRoot + 'aria2cdownload/' + usr + '/'
                os.system('tar zcvf %s.tar.gz -C %s %s' % (dirname + 'task_' + task_name, dirname, 'task_' + task_name))
                return PageResponse.file_download(dirname + 'task_' + task_name + '.tar.gz')
        except:
            return PageResponse.download_tool_error()
    else:
        return PageResponse.session_failed(request)