# Download9_Remake

Download9重制版

后台使用 `Django` 框架，数据库为 `Mariadb/Mysql`

基本配置在 `Download9/const.json` 文件中修改

运行 `python manage.py runserver 8000` 部署

## 关于数据库

请务必确保数据库开启，否则程序会抛出异常

## 关于Aria2c

aria2c未开启的情况下，将会被判定为链接不合法

## 关于AutoDelete

AutoDelete的机制基于`crontab`

使用 `python manage.py crontab add`可以开启AutoDelete

## TODO

加入了Metalink下载，还未验证可用性