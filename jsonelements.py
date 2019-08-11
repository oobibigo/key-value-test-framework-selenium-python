import json
import base64


class Elementatt(json.JSONDecoder):
    def __init__(self, dic):
        assert isinstance(dic, dict)
        self.__dict__ = dic
        # self.id = dic['id']


class Element:
    def __init__(self, dic):
        self.__dict__ = dic
        self.elementItem = []
        # self.eid = dic['eid']
        for d in dic['attribute']:
            self.elementItem.append(Elementatt(d))


class WebElementDecode:
    def __init__(self, pathstr):
        with open(pathstr, encoding='UTF-8') as fjson:
            dic = json.JSONDecoder().decode(fjson.read())
            self.__dict__ = dic
            self.elementList = []
            for ditem in dic['elements']:
                if isinstance(ditem, dict):
                    self.elementList.append(Element(ditem))


# fjson = open('SalesElements.json')

# new_element = ElementList(json.JSONDecoder.decode(str, fjson.read()))
# source = fjson.read()


'''
print(type(new_element))

print(type(new_element.elements))

print(type(new_element.elementList))

print(new_element.elementList[0].eid)

print(new_element.elementList[0].iframe)

print(new_element.elementList[0].elementItem[0].id)

print(new_element.elementList[0].elementItem[1].name)

print(new_element.name)

print(new_element.elements)
'''