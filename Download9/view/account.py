import Download9.view.pageresponse as PageResponse
import Download9.view.control as Control
import Download9.view.database as Database
import Download9.view.const as Const

def getinfo(code):
    import requests, json
    req = {"client_id" : Const.Const["Account9"]["client_id"],
           "client_secret" : Const.Const["Account9"]["client_secret"],
           "code" : code}
    res = json.loads(requests.post(url="https://accounts.net9.org/api/access_token",
                                   params=req,
                                   headers={'Content-Type': 'application/x-www-form-urlencoded'}).text)
    ret = requests.get(url="https://accounts.net9.org/api/userinfo",
                       params={"access_token": res["access_token"]})
    return json.loads(ret.text)

def account9_login(request):
    if Control.check_session(request):
        return PageResponse.jump_to_index()
    if (request.method == "GET"):
        assert request.GET.__contains__("code")
        ret = getinfo(request.GET["code"])
        try:
            Database.find_single("account", {"username": ret["user"]["name"], "password": ret["user"]["password"]})
            request.session["MemberName"] = ret["user"]["name"]
            request.session.set_expiry(Const.LoginTime)
            return PageResponse.login_success(request)
        except:
            Database.insert("account", {"username": ret["user"]["name"], "password": ret["user"]["password"], "memoryused": 0})
            request.session["MemberName"] = ret["user"]["name"]
            request.session.set_expiry(Const.LoginTime)
            return PageResponse.login_success(request)
    else:
        return PageResponse.jump_to_not_exist()

def login(request):
    if Control.check_session(request):
        return PageResponse.jump_to_index()
    if (request.method == "POST"):
        try:
            assert request.POST.__contains__("username")
            assert request.POST.__contains__("password")
            return PageResponse.login_page(request, request.POST["username"], request.POST["password"])
        except:
            return PageResponse.login_page(request, "", "")
    return PageResponse.login_page(request, "", "")

def check_login(request):
    if Control.check_session(request):
        return PageResponse.jump_to_index()
    if (request.method == "POST"):
        try:
            from Download9.getmd5 import getmd5
            pwd = getmd5(request.POST["password"])
            x = Database.find_single("account", {"username": request.POST["username"]})
            assert x[Database.id("account", "password")] == pwd
            request.session["MemberName"] = request.POST["username"]
            request.session.set_expiry(Const.LoginTime)
            return PageResponse.login_success(request)
        except:
            return PageResponse.login_failed(request, request.POST["username"], request.POST["password"])
    else:
        return PageResponse.jump_to_not_exist()

def logout(request):
    request.session.flush()
    return PageResponse.logout(request)