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
    