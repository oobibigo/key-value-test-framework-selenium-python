# key-value-test-framework-selenium-python
### 是基于selenium Python 的关键字驱动的测试框架. 
通过封装和增强selenium自带的方法, 把页面测试元素和测试数据从代码中剥离,
简化测试脚本,减少脚本的修改,提高测试脚本的稳定性和方便测试数据管理.
在迭代或变更时,通过修改,测试元素和测试数据相关的配置文件即可. 
### 使用
#### 环境
1 创建UI元素配置文件 SalesElements.json

2 设置环境相关 Setting.json

#### 脚本
通过引入模块 from TestFramework import commDriver
初始化:
cd = commDriver.CommDriver()

访问起始页:
cd.getdriver().get(self.cd.get_elementconfig().homepage)

执行UI脚本操作

新的脚本类似:
cd.getelement('ui元素ID').action()#默认click

cd.getelement('ui元素ID').action('元素对应测试数')
