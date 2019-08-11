# key-value-test-framework-selenium-python
是基于selenium Python 的关键字驱动的测试框架. 
通过封装和增强selenium自带的方法, 把页面测试元素和测试数据从代码中剥离,简化脚本减少脚本的修改,提高测试脚本的稳定性和方便测试数据管理.
在迭代或变更时,通过修改,测试元素和测试数据相关的配置文件即可. 
新的脚本类似:
page.getelement('ui元素ID').action()#默认click
page.getelement('ui元素ID').action('元素对应测试数')
