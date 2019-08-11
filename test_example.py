from TestFramework import commDriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
import datetime


class TestSequenceFunctions(unittest.TestCase):
    cd = commDriver.CommDriver()
    timestr = time.strftime("%m%d%H%M%S")
    datastr = time.strftime("%Y-%m-%d")

    @classmethod
    def setUpClass(cls):
        # 登录Sales
        print(time.strftime("%H:%M:%S"))
        cls.cd.getelement('login_username').action()
        cls.cd.getelement('login_password').action()
        cls.cd.getelement('login_loginbtn').action()

    @classmethod
    def tearDownClass(cls):
        # cls.cd.close()
        print(time.strftime("%H:%M:%S"))
        # 退出
        # if cls.cd.getelement("index_首页LOGO") is not None:
        # cls.cd.getelement('index_个人中心').action()
        # cls.cd.getelement('index_退出').action()

    def setUp(self):
        pass
        # self.cd.getdriver().get(self.cd.get_elementconfig().homepage)

    def tearDown(self):
        self.cd.getdriver().get(self.cd.get_elementconfig().homepage)

    # 清除绑定的数据
    def init_deleteblind(self):
        self.cd.getelement('index_个人中心').action()
        self.cd.getelement('账号_绑定').action()
        # tt = self.cd.getdriver().find_elements_by_class_name('unbind')
        tt = self.cd.getelements("绑定解除_解除").eidment
        for at in tt:
            if at.is_displayed() is True:
                at.click()
                time.sleep(3)
                self.cd.getelement('绑定解除_确定').action()
        self.assertTrue(self.cd.getelement("绑定解除_解除").is_element_exist())

    def test_bind_email(self):
        test_data = {'data': [{'email': 'test@test.cn', 'password': 'test'},

        self.cd.getelement('index_个人中心').action()
        self.cd.getelement('账号_绑定').action()
        for m in test_data['data']:
            self.cd.getelement('绑定email_btn').action()
            self.cd.getelement('绑定email_账号').action(m['email'])
            self.cd.getelement('绑定email_密码').action(m['password'])
            self.cd.getelement('绑定email_验证').action()
            self.cd.getelement('绑定email_立即保存').action()
            self.cd.getelement('绑定email_跳过').action()
            self.cd.getelement('绑定email_完成').action()
            # self.assertTrue(self.cd.getelement('绑定email_结果').verify_attributer(text=m['email']))
            self.assertTrue(self.cd.verifi_element('绑定email_结果', text=m['email']))
    
    def login(self):
        self.cd.getelement('login_password').action()
        self.assertTrue(self.cd.getelement("login_password").is_element_exist())

    # 导入联系人
    def test_upload_contactcvs(self):
        self.cd.getelement('index_个人中心').action()
        self.cd.getelement('账号_绑定').action()
        self.cd.getelement('CSV_上传文件').action()
        self.cd.getelement('CSV_选择文件').action("example_new.csv")
        self.cd.getelement('CSV_添加标签').action("自动化添加")
        self.cd.getelement('CSV_新建').action()
        self.cd.getelement('CSV_导入').action()
        self.cd.getelement('绑定解除_确定').action()  # ui-dialog-content 绑定解除_确定,确定按钮同样的
        self.assertTrue(self.cd.verifi_element('CSV_导入成功', text='已成功导入联系人 2 条'))
        self.cd.getelement('绑定解除_确定').action()

    # 添加联系人
    def test_add_contact(self):
        test_data = {'名': 'robot', '姓': 'py', '头衔': 'AFO', '邮箱': 'robot', '手机': '18013131313'}
        # range(1,10)
        i = 1
        m = test_data
        self.cd.getelement('导航_联系').action()
        # for m in test_data:
        while i <= 3:
            self.cd.getelement('联系_新增联系人').action()
            timestr = time.strftime("%m%d%H%M%S")
            self.cd.getelement('联系_姓').action("{0}{1}{2}".format(m['名'], timestr, i))
            self.cd.getelement('联系_名').action(m['姓'])
            self.cd.getelement('联系_头衔').action(m['头衔'])
            # self.cd.getelement('联系_公司').action()
            self.cd.getelement('联系_邮箱').action("{0}{1}{2}@1.com".format(m['邮箱'], timestr, i))
            self.cd.getelement('联系_手机').action(m['手机'] + str(i))
            self.cd.getelement('联系_保存').action()
            # self.assertTrue(self.cd.getelement('联系详情_邮件').verify_attributer(text=m['邮箱']))
            self.assertTrue(self.cd.verifi_element('联系详情_邮件', text=m['邮箱']))
            self.add_tagcontact()
            i += 1

    # 给联系人添加标签
    def add_tagcontact(self):
        self.cd.getelement('联系详情_添加标签').action()
        self.cd.getelement('联系详情_标签输入').action('Robotadd')
        self.cd.getelement('联系详情_名称').action()
        self.cd.getelement('联系详情_标签保存').action()  # 标签控件需要点击两次才能添加成功
        # self.assertTrue(self.cd.getelement('联系详情_标签列表').verify_attributer(text='Robotadd'))
        self.assertTrue(self.cd.verifi_element('联系详情_标签列表', text='Robotadd'))

    # 添加公司
    def test_add_company(self):
        self.cd.getelement('导航_联系').action()
        comstr = "Tcom{0}".format(time.strftime("%m%d%H%M%S"))
        website = "www.c{0}.com".format(time.strftime("%m%d%H%M%S"))
        self.cd.getelement('联系_添加公司').action()
        self.cd.getelement('联系_公司名称').action(comstr)
        self.cd.getelement('联系_公司网址').action(website)
        self.cd.getelement('联系_公司保存').action()
        # self.assertTrue(self.cd.verifi_element("toastmsg", text='添加成功'))
        self.assertTrue(self.cd.verifi_element("联系详情_公司名称", text=comstr))
        self.assertTrue(self.cd.verifi_element("联系详情_公司网址", text=website))

    # 添加商机
    def test_add_deals(self):
        for i in range(0, 1):
            idres = i
            if idres > 2:
                idres = 0
            d1 = datetime.datetime.now()
            d2 = d1 + datetime.timedelta(days=1 + i)
            amountint = i + 50
            titlestr = '自动化商机{0}_{1}'.format(self.timestr, i)
            self.cd.getelement('导航_商机').action()
            self.cd.getelement('商机_新建商机').action()
            self.cd.getelement('商机_商机表单_显示更多').action(titlestr)
            self.cd.getelement('商机_商机表单_名称').action(titlestr)
            self.cd.getelement('商机_商机表单_相关人员').action('Denis Zhang')
            # self.cd.getelement('商机_商机表单_相关公司').action()
            self.cd.getelement('商机_商机表单_金额').action(amountint)
            self.cd.getelement('商机_商机表单_预计完成日期').action(d2.strftime('%Y-%m-%d'))
            self.cd.getelement('商机_商机表单_成功率').action('select', index=i)
            self.cd.getelement('商机_商机表单_当前阶段').action('select', index=i)
            self.cd.getelement('商机_商机表单_负责人').action('select', index=idres)
            self.cd.getelement('商机_商机表单_备注').action('商机的备注信息，自动化的备注日期：{0}'.format(titlestr))
            self.cd.getelement('商机_商机表单_保存').action()
            self.assertTrue(self.cd.verifi_element('商机_商机详情_标题', text=titlestr))
            # self.set_deal_status(titlestr, 1)
            self.set_deal_status(titlestr, 2)

    # 设置商机完成状态 titlestrs根据标题修改,status 1 成功 2 失败 3 删除
    def set_deal_status(self, titlestr, status=1):
        self.cd.getelement('导航_商机').action()
        self.cd.getelement('商机列表_标题', text=titlestr).action()
        self.cd.getelement('商机详情_设置状态菜单V').action()
        if status is 1:
            self.cd.getelement('商机详情_设置成功').action()
            self.cd.getelement('商机详情_成功金额click').action()
            self.cd.getelement('商机详情_成功金额').action('20')
            self.cd.getelement('商机详情_成功日期').action(self.datastr)
            self.cd.getelement('商机详情_成交总结').action('自动化成交的商机,时间：' + self.timestr)
            self.cd.getelement('商机详情_成功金额click').action()
            self.cd.getelement('商机详情_成交保存').action()
            # self.assertTrue(self.cd.verifi_element("toastmsg", text='操作成功')) # 这个元素没有用，验证不通过
            self.assertTrue(self.cd.verifi_element('商机_商机详情_标题', text=titlestr))
            self.assertTrue(self.cd.verifi_element('商机详情_商机成功状态', text='成功'))
        elif status is 2:
            self.cd.getelement('商机详情_设置失败').action()
            self.cd.getelement('商机详情_失败日期').action(self.datastr)
            self.cd.getelement('商机详情_失败原因').action('自动化设置商机失败原因，时间：' + self.timestr)
            self.cd.getelement('商机详情_失败保存').action()
            # self.assertTrue(self.cd.verifi_element("toastmsg", text='操作成功'))
            self.assertTrue(self.cd.verifi_element('商机_商机详情_标题', text=titlestr))
            self.assertTrue(self.cd.verifi_element('商机详情_商机失败状态', text='失败'))
        elif status is 3:
            self.cd.getelement('商机详情_删除商机').action()
            self.cd.getelement('商机详情_对话框').action()
            self.cd.getelement('商机详情_删除确定').action()
            self.assertFalse(self.cd.verifi_element('商机列表_标题', text=titlestr))  # 删除后就找不到标题了
            # self.assertTrue(self.cd.verifi_element("toastmsg", text='删除成功'))

    # 添加任务
    def test_add_task(self):
        titlestr = '自动化新建任务{0}'.format(self.timestr)
        self.cd.getelement('导航_任务').action()
        self.cd.getelement('任务_新建任务').action()
        self.cd.getelement('任务_主题').action(titlestr)
        self.cd.getelement('任务_描述').action('任务的新描述')
        self.cd.getelement('任务_到期时间').action('select', index=4)
        self.cd.getelement('任务_指派给').action('select', index=0)
        self.cd.getelement('任务_相关人员').action('Denis Zhang')
        self.cd.getelement('任务_商机').action('不动产商机')
        self.cd.getelement('任务_标签').action('1自动化的任务标签')
        self.cd.getelement('任务_任务文本').action()
        self.cd.getelement('任务_保存').action()
        self.cd.getdriver().refresh()
        self.assertTrue(self.cd.verifi_element("任务_列表任务标题", text=titlestr))
        self.set_task_status(titlestr)

    # 设置任务完成状态
    def set_task_status(self, titlestr):
        self.cd.getelement('导航_任务').action()
        self.cd.getelement('任务_选择标签').action('select', index=1)
        # self.cd.getelement('任务_列表任务状态更新').action()
        temp = self.cd.getelement('任务_列表任务状态自定义', text=titlestr)
        temp.eidment.find_element_by_tag_name('span').click()
        self.assertTrue(self.cd.verifi_element("toastmsg", text='设置成功'))

    # 发现，公司搜索
    def test_search_company(self):
        self.cd.getelement('导航_发现').action()
        self.cd.getelement('导航_发现_Company').action()
        self.search_keyword(1, 'nike', 'jobs.nike.com')

    # 发现，公司人员搜索
    def test_search_people(self):
        self.cd.getelement('导航_发现').action()
        self.cd.getelement('导航_发现_People').action()
        self.search_keyword(2, 'nike.com', 'Nike, Inc.')

    # 发现索，社交搜索
    def test_search_social(self):
        self.cd.getelement('导航_发现').action()
        self.cd.getelement('导航_发现_Social').action()
        self.search_keyword(3, 'nike', 'Just Do It')

    def search_keyword(self, i, keyword, vifistr):
        self.cd.getelement('发现_搜索内容').action(keyword)
        self.cd.getelement('发现_搜索内容').action(key=Keys.ENTER)
        if i is 1:
            self.assertTrue(self.cd.verifi_element("发现_公司搜索结果", text=vifistr))
            self.cd.getelement('发现_公司搜索结果_人员搜索').action()
            self.assertTrue(self.cd.verifi_element("发现_公司搜索结果_人员搜索_匹配公司名称", text='Nike, Inc'))
            self.cd.close()
        elif i is 2:
            self.cd.getelement('发现_公司搜索结果_人员搜索_显示更多').action()
            self.assertTrue(self.cd.verifi_element("发现_公司搜索结果_人员搜索_匹配公司名称", text=vifistr))
        elif i is 3:
            self.assertTrue(self.cd.verifi_element("发现_社交搜索_FBres", text=vifistr))
            self.cd.getelement('发现_社交搜索_Twitter').action()
            self.assertTrue(self.cd.verifi_element("发现_社交搜索_Twres", text='http://www.nike.com'))
            self.cd.getelement('发现_社交搜索_LinkedIn').action()
            self.assertTrue(self.cd.verifi_element("发现_社交搜索_Lkres", text='NIKE, Inc. is the world\'s leading designer'))
            self.cd.getelement('发现_社交搜索_Facebook').action()


if __name__ == '__main__':
    unittest.main()
