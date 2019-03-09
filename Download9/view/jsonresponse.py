import json
from Download9.view.const import HintContext, HintTitle
from django.shortcuts import HttpResponse

def download_tool_error():
    return HttpResponse(json.dumps({"result": "fail",
                                    "title": HintTitle["Wrong"],
                                    "context": [HintContext["UrlError"], HintContext["PleaseChange"]],
                                    "nexturl": ""}))

def upload_btfile_empty():
    return HttpResponse(json.dumps({"result": "fail",
                                    "title": HintTitle["Wrong"],
                                    "context": [HintContext["UploadBTFileEmpty"], HintContext["PleaseRetry"]],
                                    "nexturl": ""}))

def upload_btfile_toolarge():
    return HttpResponse(json.dumps({"result": "fail",
                                    "title": HintTitle["Wrong"],
                                    "context": [HintContext["UploadBTFileTooLarge"], HintContext["PleaseChangeFile"]],
                                    "nexturl": ""}))

def memory_limit_exceeded():
    return HttpResponse(json.dumps({"result": "failed",
                                    "title": HintTitle["Wrong"],
                                    "context": [HintContext["MemoryUseExceeded"], HintContext["ForcePaused"]],
                                    "nexturl": "/index"}))

def task_number_exceeded():
    return HttpResponse(json.dumps({"result": "fail",
                                    "title": HintTitle["Wrong"],
                                    "context": [HintContext["TaskNumberExceeded"]],
                                    "nexturl": ""}))

def task_name_repeated():
    return HttpResponse(json.dumps({"result": "fail",
                                    "title": HintTitle["Wrong"],
                                    "context": [HintContext["TaskNameRepeated"], HintContext["PleaseChange"]],
                                    "nexturl": ""}))

def session_failed():
    return HttpResponse(json.dumps({"result": "session_failed",
                                    "title": HintTitle["Wrong"],
                                    "context": [HintContext["NeedLogin"], HintContext["JumpToIndex"]],
                                    "nexturl": "/login"}))

def get_overall_state(overall_cnt, memory):
    return HttpResponse(json.dumps({"result": "success",
                                    "overall_cnt": overall_cnt,
                                    "memory_used": int(memory / 1024 / 1024)}))

def need_refresh():
    return HttpResponse(json.dumps({"result": "success",
                                    "refresh": "1"}))

def get_tasks_state(req_all, download_cnt, overall_cnt, memory):
    return HttpResponse(json.dumps({"result": "success",
                                    "data": req_all,
                                    "download_cnt": download_cnt,
                                    "overall_cnt": overall_cnt,
                                    "memory_used": int(memory / 1024 / 1024)}))

def operation_success():
    return HttpResponse(json.dumps({"result": "success",
                                    "title": HintTitle["Success"],
                                    "context": [HintContext["OperationSuccess"]],
                                    "nexturl": "/index"}))