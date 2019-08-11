import json


class CommSetting:
    inst = object

    def __init__(self):
        with open('Setting.json', encoding='UTF-8') as fjson:
            dic = json.JSONDecoder().decode(fjson.read())
            self.__dict__ = dic

    @staticmethod
    def getset():
        if isinstance(CommSetting.inst, CommSetting):
            return CommSetting.inst
        else:
            CommSetting.inst = CommSetting()
            return CommSetting.inst



# print(CommSetting.getset().browserdriverpath)

# print(CommSetting.getset().browserdriverpath)
