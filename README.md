# simple_scraper
Freebuf.com : 简化版线程池爬虫。a threadpool scraper from freebuf

使用说明:
class Scraper:
	def __init__(self, single_page = True, workers_num = 8, worker_class):
		single_page:当前爬虫模式是单页面还是多页面
		workers_num:当前多页面爬虫线程数
		worker_class:当前爬虫实际工作处理页面的类（可以自定义）

	def get_result_elements_queue(self):
		返回值：Queue.Queue
		调用该方法返回一个队列，该队列存储自定义结果
	def get_result_urls_queue(self):
		返回值：Queue.Queue
		调用该方法返回一个队列，该队列存储默认结果

	def kill_woker(self):
		结束所有进程

	def feed(self, target_urls):
		target_urls是你希望爬虫处理的url
		可以多次feed,可以传入一个字符串形式的url也可以传入一个list,list包含多个str形式的url

class ScraperWorkerBase:
	用户需求比较低时，基本默认的该类就可以满足要求，但是如果需求需要定制，请复写该类，并将类作为参数传入worker_class
	def parse_page(self)
		通过继承并复写这个方法来自定义处理页面，
		self.soup是该页面的bs4的soup对象，同样，大家可以修改源代码让它支持更多的类型解析

	def __get_html_data(self)
		通过继承复写该函数可以修改认证过程，使用特定需要。


使用实例：
一：
#encoding:utf-8
from scraper import *
import Queue
import time
import sys
import bs4

test_obj = Scraper(single_page=False, workers_num=15)
test_obj.feed(['http://freebuf.com'])
time.sleep(5)
z = test_obj.get_result_urls_queue()

while True:
    try :
        print z.get(timeout=4)
    except:
        pass
    
二：
#encoding:utf-8
from scraper import *
import Queue
import time
import sys
import bs4

class MyWorker(ScraperWorkerBase):
    
    def parse_page(self):
        all_tags = self.soup.find_all('img')
        for i in all_tags:
            print i
            
        return 

test_obj = Scraper(single_page=False, worker_class=MyWorker)
test_obj.feed(['http://uestc.edu.cn'])
time.sleep(5)
z = test_obj.get_result_urls_queue()
x = test_obj.get_result_elements_queue()
while True:
    try :
        print z.get(timeout=4)
        element_set = x.get(timeout=2)
        for i in element_set:
            print i
    except:
        pass
    

	
