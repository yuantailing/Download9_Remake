import json, os

ConstJson = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'const.json'), 'r', encoding='utf8')
Const = json.load(ConstJson)
AriaAddress = Const["AriaAddress"]
HintTitle = Const["Hint"]["Title"]
HintContext = Const["Hint"]["Context"]
DownloadRoot = Const["DownloadRoot"]
MemoryLimit = Const["MemoryLimit"]
TaskNumberLimit = Const["TaskNumberLimit"]
DatabaseInfo = Const["Database"]
LoginTime = Const["Session"]["LoginTime"]