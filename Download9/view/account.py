import Download9.view.pageresponse as PageResponse
import Download9.view.control as Control
import Download9.view.database as Database
import Download9.view.const as Const

def getinfo(code):
    import requests, json
    return {'user': {'name': 'testuser-1', 'password': '000000'}}
    req = {"client_id" : Const.Const["Account9"]["client_id"],
           "client_secret" : Const.Const["Account9"]["client_secret"],
           "code" : code}
    '''printf('    a9test_step0')'''
    res = json.loads(requests.post(url="https://accounts.net9.org/api/access_token",
                                   params=req,
                                   headers={'Content-Type': 'application/x-www-form-urlencoded'}).text)
    '''printf('    a9test_step1')'''
    ret = requests.get(url="https://accounts.net9.org/api/userinfo",
                       params={"access_token": res["access_token"]})
    '''printf('    a9test_step2')'''
    return json.loads(ret.text)

'''
def printf(s):
    f = open('/home/dwn9/Download9_Remake/debug.log', 'a')
    f.write(s)
    f.write('\n')
    f.close()
'''

def account9_login(request):
    if Control.check_session(request):
        return PageResponse.jump_to_index()
    if (request.method == "GET"):
        '''
        printf('')
        printf('a9test_begin')
        '''
        #assert request.GET.__contains__("code")
        '''printf('a9test_start_get_info')'''
        ret = getinfo(request.GET.get('code'))
        '''printf('a9test_end_get_info')'''
        try:
            '''printf('a9test_try_read_old_account')'''
            Database.find_single("account", {"username": ret["user"]["name"], "password": ret["user"]["password"]})
            '''printf('a9test_start_setting_session')'''
            request.session["MemberName"] = ret["user"]["name"]
            request.session.set_expiry(Const.LoginTime)
            '''printf('a9test_auth_over')'''
            return PageResponse.login_success(request)
        except:
            '''printf('a9test_try_inser_new_account')'''
            Database.insert("account", {"username": ret["user"]["name"], "password": ret["user"]["password"], "memoryused": 0})
            '''printf('a9test_start_setting_session')'''
            request.session["MemberName"] = ret["user"]["name"]
            request.session.set_expiry(Const.LoginTime)
            '''printf('a9test_auth_over')'''
            return PageResponse.login_success(request)
    else:
        '''printf('a9test_end:get_session failed')'''
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
