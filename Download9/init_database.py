from Download9.view.const import DatabaseInfo
import MySQLdb

HOST = DatabaseInfo["Host"]
USER = DatabaseInfo["Username"]
PASSWD = DatabaseInfo["Password"]
DB = DatabaseInfo["Database"]
CHARSET = "utf8"

db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB, charset=CHARSET)

cursor = db.cursor()
'''print("CREATE TABLE IF NOT EXISTS account("
      + "username CHAR(40) NOT NULL,"
      + "password CHAR(40) NOT NULL,"
      + "memoryused BIGINT UNSIGNED,"
      + "PRIMARY KEY ( username )"
      + ")CHARSET=utf8;")'''

cursor.execute("CREATE TABLE IF NOT EXISTS account("
               + "username CHAR(40) NOT NULL,"
               + "password CHAR(40) NOT NULL,"
               + "memoryused BIGINT UNSIGNED,"
               + "PRIMARY KEY ( username )"
               + ")CHARSET=utf8;")

'''print("CREATE TABLE IF NOT EXISTS task("
      + "username CHAR(40) NOT NULL,"
      + "gid CHAR(40) NOT NULL,"
      + "taskname CHAR(40) NOT NULL,"
      + "createtime CHAR(10) NOT NULL,"
      + "attr TINYINT NOT NULL"
      + ")CHARSET=utf8;")'''

cursor.execute("CREATE TABLE IF NOT EXISTS task("
               + "username CHAR(40) NOT NULL,"
               + "gid CHAR(40) NOT NULL,"
               + "taskname CHAR(40) NOT NULL,"
               + "createtime CHAR(10) NOT NULL,"
               + "attr TINYINT NOT NULL"
               + ")CHARSET=utf8;")