import logging
import time
from collections import Iterable
from selenium.common import exceptions
from TestFramework import jsonelements
from TestFramework import commSetting
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec


class CommDriver:
    setobj = commSetting.CommSetting.getset()
    currentelement = object
    main_handle = None

    def __init__(self):
        # 初始化元素库
        self.__webelements = jsonelements.WebElementDecode(self.setobj.webelementpath)
        self.eidment = None
        self.__eid = ''
        self.__iframe = ''
        self.__windows = ''
        self.__verifi_att = ''
        self.__verifi_value = ''
        self.__action = ''
        self.__actionvalue = ''
        chromestr = self.setobj.browserdriverpath
        # 设置driver属性
        tiemset = 60
        self.__cDriver = webdriver.Chrome(chromestr)
        self.__cDriver.set_page_load_timeout(tiemset)
        self.__cDriver.set_script_timeout(tiemset)
        self.__cDriver.implicitly_wait(tiemset)
        self.__cDriver.maximize_window()
        self.wait = WebDriverWait(self.__cDriver, 20)
        self.__cDriver.get(self.__webelements.homepage)
        self.main_handle = self.__cDriver.current_window_handle
        # 设置日志
        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='runException.log',
                            filemode='w')

    def get_elementconfig(self):
        return self.__webelements

    def __del__(self):
        self.__cDriver.close()

    def getdriver(self):
        self.__cDriver.switch_to.window(self.__cDriver.current_window_handle)
        return self.__cDriver

    def getelements(self, elementid, multi=2):
        return self.getelement(elementid, multi)

    # 获取页面元素
    def getelement(self, elementid, multi=1, **kw):  # multi = 是否返回多个，默认返回一个
        for ets in self.__webelements.elementList:  # 获取对应的ID值
            if elementid == ets.eid:
                self.__eid = ets.eid
                self.__iframe = ets.iframe
                self.__windows = ets.windows
                self.__verifi_att = ets.verifi_att
                self.__verifi_value = ets.verifi_value
                self.__action = ets.action
                self.__actionvalue = ets.actionvalue
                self.__setwinframe(ets)
                # 用户自定义输入的字符查找元素
                if kw is not None:
                    if kw.get('text') is not None:  # 匹配元素文本
                        # if str(self.eidment.text).find(kw.get('text')) >= 0:
                        ets.elementItem[-1].text = kw.get('text')
						# [-1]属性的最后一项使用用户自定义的输入的内容来匹配
                    elif kw.get('att') is not None:  # 匹配元素属性值
                        varstr = str(kw.get('att')).replace('__', '-')  # 横杠用双下划线代替
                        ets.elementItem[-1].att = varstr
                        ets.elementItem[-1].attvalue = kw.get('attvalue')
                self.eidment = self.__findelemnt(ets.elementItem, multi)

                return self

    # 验证页面元素和对应的值是否存在
    def verifi_element(self, elementid, **kw):
        self.getelement(elementid, **kw)
        return self.is_element_exist()

    # 设置切换元素窗口和iframe
    def __setwinframe(self, ets):
        self.__cDriver.switch_to.window(self.__cDriver.current_window_handle)
        if len(ets.windows) != 0 and len(self.__cDriver.window_handles) > 1:
            try:
                wi = 0
                if ets.windows.isdigit():  # 如果窗口参数是数字，通过循环所有窗口选择对应的窗口
                    tempwi = int(ets.windows)
                    for handle in self.__cDriver.window_handles:
                        if wi == tempwi:
                            self.__cDriver.switch_to.window(handle)
                        wi += 1
                else:
                    self.__cDriver.switch_to.window(ets.windows)
            except exceptions.NoSuchWindowException:
                self.__cDriver.save_screenshot(self.setobj.testimgpath + 'find_' + self.__eid +
                                              '_window' + self.__windows + '_error.png')
                self.__cDriver.switch_to.default_content()
                logging.warning('在网页:[' + self.__cDriver.current_url + ']找不到窗口:[' +
                                self.__windows + '][' + self.__eid + ']')
        if len(ets.iframe) != 0:
            try:
                self.__cDriver.switch_to.default_content()
                if ets.iframe.isdigit():
                    self.__cDriver.switch_to.frame(int(ets.iframe))
                elif isinstance(ets.iframe, str) and ets.iframe.find('findiframe_') is False:
                    self.__cDriver.switch_to.frame(ets.iframe)
                else:
                    self.__cDriver.switch_to.frame(self.__cDriver.find_elements_by_tag_name('iframe')[0])
            except Exception as ex:
                self.__cDriver.get_screenshot_as_file(self.setobj.testimgpath + 'find_' + self.__eid +
                                                     '_iframe' + self.__iframe + '_error.png')
                self.__cDriver.switch_to.default_content()
                logging.warning('在网页:[' + self.__cDriver.current_url + ']找不到iframe:[' +
                                self.__iframe + '][' + self.__eid + ']')

    # 遍历查找元素
    def __findelemnt(self, element, multi):
        if isinstance(element, Iterable) is False:
            print('错误的Item:' + element)
            return None
        tempdriver = self.__cDriver
        for e in element:
            if tempdriver is None:
                return None
            # 匹配到最后一项为止
            if isinstance(tempdriver, Iterable) is False:
                tempdriver = self.__findatt(tempdriver, e)
            else:
                tempdriver = self.__findatt(tempdriver[0], e)
        # multi=2 getelements调用返回全部元素
        if multi == 2:
            return tempdriver
        else:
            if tempdriver is not None and isinstance(tempdriver, list):
                return tempdriver[0]
            else:
                return tempdriver

    def __findatt(self, cdriver, element):
        bytuple = ()  # 匹配元素的元组
        if len(element.id) != 0:
            bytuple = (By.ID, element.id)
        elif len(element.name) != 0:
            bytuple = (By.NAME, element.name)
        elif len(element.linktext) != 0:
            bytuple = (By.LINK_TEXT, element.linktext)
        elif len(element.tagname) != 0:
            bytuple = (By.TAG_NAME, element.tagname)
        elif len(element.classname) != 0:
            bytuple = (By.CLASS_NAME, element.classname)
        elif len(element.css_selector) != 0:
            bytuple = (By.CSS_SELECTOR, element.css_selector)
        elif len(element.xpath) != 0:
            bytuple = (By.XPATH, element.xpath)

        findwait = WebDriverWait(cdriver, 20)

        # 根据元素属性对应的值获取元素
        if len(element.att) > 0:
            try:
                return findwait.until(ec.elements_have_atttext_element(bytuple, element.att, element.attvalue))
            except exceptions.TimeoutException as ex:
                self.__cDriver.save_screenshot(self.setobj.testimgpath + 'find_' + self.__eid + '_element' + '_error.png')
                logging.warning('在网页:[' + self.__cDriver.current_url + ']中找不到元素:[' +
                                   self.__eid + ']的属性值不能匹配[' + element.att + ']=[' + element.attvalue + ']=[' + str(ex) + ']')
                return None

        # 根据元素的text文本值获取元素
        if len(element.text) > 0:
            try:
                return findwait.until(ec.elements_have_text_element(bytuple, element.text))
            except exceptions.TimeoutException as ex:
                self.__cDriver.save_screenshot(self.setobj.testimgpath + 'find_' + self.__eid + '_element' + '_error.png')
                logging.warning('在网页:[' + self.__cDriver.current_url + ']中找不到元素:[' +
                                self.__eid + ']的文本不能匹配[' + element.text + ']=[' + str(ex.args) + ']')
                return None

        # 元素没有属性值和文本匹配,按默认的条件进行搜索
        tempelist = []
        try:
            tempelist = findwait.until(ec.presence_of_all_elements_located(bytuple))
        except exceptions.TimeoutException or exceptions.WebDriverException as ex:
            self.__cDriver.save_screenshot(self.setobj.testimgpath + 'find_' + self.__eid + '_element' + '_error.png')
            logging.warning('在网页:[' + self.__cDriver.current_url + ']中找不到元素:[' +
                            self.__eid + '][' + str(element.__dict__) + ']errMsg:[' + str(ex) + ']')
            return None
        # 如果返回的元素列表有值就返回
        if len(tempelist) > 0:
            return tempelist
        else:
            return None

    # astr元素输入的值，默认是空.select 元素,使用 action('xxx',index=1)来操作
    def action(self, astr=None, **kw):
        if self.eidment is None:
            logging.warning("元素是空的，不能执行action")
            return
        try:
            if astr is not None:
                inputstr = astr
            else:
                inputstr = self.__actionvalue
            if kw is not None and kw.get('key') is not None:  # 用户输入键盘
                self.eidment.send_keys(kw.get('key'))
            elif self.__action == 'click':
                self.eidment.click()
            elif self.__action == 'input':
                # self.eidment.click()
                self.eidment.clear()
                self.eidment.send_keys(inputstr)
            elif self.__action == 'select':
                thesel = Select(self.eidment)
                if kw is not None:
                    if kw.get('index') is not None:  # 匹配下拉列表的index
                        thesel.select_by_index(kw.get('index'))
                    if kw.get('value') is not None:  # 匹配 foo <option value=”foo”>Bar</option>
                        thesel.select_by_value(kw.get('value'))
                    if kw.get('text') is not None:
                        thesel.select_by_visible_text(kw.get('text'))
            else:
                logging.warning(self.__eid + "动作没设置或者不支持此方法，检查json ACTION设置")
            self.eidment = None
        except Exception as we:
            self.eidment = None
            logging.warning(self.__eid + ":动作执行异常")
            logging.warning(we.args)

    # 验证元素的值是否存在
    # **kw 输入自定义的验证字符。text = 'a' 验证文本， att='id',att_value='30010' 验证元素属性值
    def verify_attributer(self, **kw):
        if self.eidment is None:
            logging.warning("元素是空的，不能对比attribute")
            return False
        # 用户有输入匹配的字符
        if kw is not None:
            if kw.get('text') is not None:  # 匹配元素文本
                # if str(self.eidment.text).find(kw.get('text')) >= 0:
                return self.__text_match(kw.get('text'))
            elif kw.get('att') is not None:  # 匹配元素属性值
                return self.__attr_match(kw.get('att'), kw.get('att_value'))
            else:
                print('参数输入有误:' + kw)
                logging.warning('参数输入有误:' + kw)
                return False
        # 匹配公共元素库中的值
        if len(self.__verifi_att) > 0 and self.__verifi_att.find('text') == -1:  # 匹配元素属性值
            return self.__attr_match(self.__verifi_att, self.__verifi_value)
        else:
            return self.__text_match(self.__verifi_value)
        return False

    def __attr_match(self, att, verfivalue):  # 匹配元素属性对应的值
        if isinstance(self.eidment, Iterable):  # 返回了多个元素，则每个元素去匹配值
            for eitem in self.eidment:
                eleatt = eitem.get_attribute(att)
                if eleatt is not None and str(eleatt).find(verfivalue) >= 0:
                    return True
            return False
        else:
            iatt = self.eidment.get_attribute(att)
            if iatt is not None and str(iatt).find(verfivalue) >= 0:
                return True
            else:
                return False

    def __text_match(self, verfitext):  # 匹配元素文本的值
        if isinstance(self.eidment, Iterable):  # 返回了多个元素，则每个元素去匹配值
            for eitem in self.eidment:
                eleatt = eitem.text
                if eleatt is not None and str(eleatt).find(verfitext) >= 0:
                    return True
            return False
        else:
            iatt = self.eidment.text
            if iatt is not None and str(iatt).find(verfitext) >= 0:  # 单个元素去匹配
                return True
            else:
                return False

    # 查找元素是否存在
    def is_element_exist(self):
        return True if self.eidment is not None else False

    def getelementattribute(self):
        if self.eidment is '':
            logging.warning("元素是空的，不能查找attribute")
            return False
        if len(self.__verifi_att) > 0:
            return self.get_attribute(self.__verifi_att)
        else:
            return False

    def close(self):
        self.__cDriver.close()
        self.__cDriver.switch_to.window(self.main_handle)

# print(CommDriver('SalesElements.json').getelement('searchbtn').verify_attributer())
# print(CommDriver('SalesElements.json').getelement('searchbtn').getelementattribute())
# CommDriver('SalesElements.json').getelement('ruomilink').action()
# cd = CommDriver()
# cd.getelement('searchinput').action()
# cd.getelement('searchbtn').action()
# cd.getelement('searchinput').action('kaka')
# cd.getelement('searchbtn').action()
# time.sleep(10)
