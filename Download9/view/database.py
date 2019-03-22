from Download9.view.const import DatabaseInfo
import MySQLdb
HOST = DatabaseInfo["Host"]
USER = DatabaseInfo["Username"]
PASSWD = DatabaseInfo["Password"]
DB = DatabaseInfo["Database"]
CHARSET = "utf8"

import threading

def id(Table, Column):
    if (Table == "account"):
        if (Column == "username"):
            return 0
        elif (Column == "password"):
            return 1
        elif (Column == "memoryused"):
            return 2
        else:
            assert 0
    elif (Table == "task"):
        if (Column == "username"):
            return 0
        elif (Column == "gid"):
            return 1
        elif (Column == "taskname"):
            return 2
        elif (Column == "createtime"):
            return 3
        elif (Column == "attr"):
            return 4
        else:
            assert 0
    else:
        assert 0

def run(Str, NeedResult = True):
    db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB, charset=CHARSET)
    lock = threading.Lock()
    lock.acquire()
    cursor = db.cursor()
    try:
        cursor.execute(Str)
        db.commit()
        if (NeedResult):
            ret = cursor.fetchall()
    except:
        db.rollback()
    cursor.close()
    lock.release()
    if (NeedResult):
        return ret

def get_all(Table, Rules):
    if (len(Rules) == 0):
        return run("SELECT * FROM " + Table + ";")
    s = ""
    for (i, j) in Rules.items():
        if isinstance(j, str):
            j = "\"" + j + "\""
        s = s + i + "=" + j + " AND "
    return run("SELECT * FROM " + Table + " WHERE " + s[:-5] + ";")

def find_single(Table, Rules):
    res = get_all(Table, Rules)
    assert len(res) == 1
    return res[0]

def check_exist(Table, Rules):
    res = get_all(Table, Rules)
    return len(res) > 0

def update(Table, Object, NewArgv):
    if (len(Object) == 0) or (len(NewArgv) == 0): return
    Objects = ""
    for (i, j) in Object.items():
        if isinstance(j, str):
            j = "\"" + j + "\""
        Objects = Objects + i + "=" + str(j) + " AND "
    NewArgvs = ""
    for (i, j) in NewArgv.items():
        if isinstance(j, str):
            j = "\"" + j + "\""
        NewArgvs = NewArgvs + i + "=" + str(j) + ","
    run("UPDATE " + Table + " SET " + NewArgvs[:-1] + " WHERE " + Objects[:-5] + ";", False)

def delete(Table, Rules):
    if (len(Rules) == 0): return
    s = ""
    for (i, j) in Rules.items():
        if isinstance(j, str):
            j = "\"" + j + "\""
        s = s + i + "=" + str(j) + " AND "
    run("DELETE FROM " + Table + " WHERE " + s[:-5] + ";", False)

def insert(Table, Object):
    if (len(Object) == 0): return
    Fields = "("
    Values = "("
    for (i, j) in Object.items():
        if isinstance(j, str):
            j = "\"" + j + "\""
        Fields = Fields + i + ","
        Values = Values + str(j) + ","
    Fields = Fields[:-1] + ")"
    Values = Values[:-1] + ")"
    run("INSERT INTO " + Table + " " + Fields + " VALUES " + Values + ";", False)
