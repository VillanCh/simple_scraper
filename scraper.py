#encoding:utf-8
import threading
import Queue
import urlparse
import requests
import bs4

class ScraperWorkerBase(object):
    """
    No needs to learn how is work,
    rewrite parse_page using self.soup(Beautiful), and return result,
    you can get the result by using
    
        (inpage_urls, your_own_result) urlscraper.execute()
    """
    def __init__(self, url = ''):
        
        self.target_url = url
        self.netloc = urlparse.urlparse(self.target_url)[1]
        
        
        self.response = None
        self.soup = None
        
        self.url_in_site = []
        self.url_out_site = []
        
    def __get_html_data(self):
        try:
            self.response = requests.get(self.target_url, timeout = 5)
        except:
            return ""
        
        print "[_] Got response"
        return self.response.text
    def __get_soup(self):
        text = self.__get_html_data()
        if text == '':
            return []
        
        return bs4.BeautifulSoup(text)
    
        #return soup
        
    def __get_all_url(self):
        url_lists = []
        
        self.soup = self.__get_soup()
        if isinstance(self.soup, type(None)):
            return []
        
        all_tags = self.soup.findAll("a")
        for a in all_tags:
            try:
                #print a['href']
                url_lists.append(a["href"])
            except:
                pass
            
        return url_lists
    def get_urls_inpage(self):
        ret_list = self.__get_all_url()
        
        if ret_list == []:
            return ([],[])
        else:
            for url in ret_list:
                o = urlparse.urlparse(url)
                #
                #print url
                if self.netloc in o[1]:
                    self.url_in_site.append(o.geturl())
                else:
                    self.url_out_site.append(o.geturl())
                    
        inurlset = set(self.url_in_site)
            
        outurlset = set(self.url_out_site)
            
        return inurlset, outurlset


    def execute(self):
        inpage_url = self.get_urls_inpage()
        undefined_result = self.parse_page()

        return inpage_url, undefined_result
    
    
    def parse_page(self):
        pass
        
        

class Scraper(object):
    def __init__(self, single_page = True,  workers_num = 8, worker_class = ScraperWorkerBase):
        self.count = 0
        self.workers_num = workers_num
        
        """get worker_class"""
        self.worker_class = worker_class
        
        """check if the workers should die"""
        self.all_dead = False
        
        """store the visited pages"""
        self.visited = set()
        
        """by ScraperWorkerBase 's extension result queue"""
        self.result_urls_queue = Queue.Queue()
        self.result_elements_queue = Queue.Queue()
        
        """
        if single_page == True, 
        the task_queue should store the tasks (unhandled)
        """
        self.task_queue = Queue.Queue()
        
        self.single_page = single_page
        if self.single_page == False:
            self.__init_workers()
        else:
            self.__init_single_worker()
        
    def __check_single_page(self):
        if self.single_page == True:
            raise StandardError('[!] Single page won\'t allow you use many workers')
        

    """init worker(s)"""
    def __init_single_worker(self):
        ret = threading.Thread(target=self._single_worker)
        ret.start()
    def __init_workers(self):
        self.__check_single_page()
        
        for _ in range(self.workers_num):
            ret = threading.Thread(target=self._worker)
            ret.start()
        
            
            
        

    """return results"""
    def get_result_urls_queue(self):
        
        
        return self.result_urls_queue
    def get_result_elements_queue(self):
        
        return self.result_elements_queue
      

    """woker function"""
    def _single_worker(self):
        if self.all_dead != False:
            self.all_dead = False
        scraper = None
        while not self.all_dead:
            try:
                
                url = self.task_queue.get(block=True)
                print 'Workding', url
                try:
                    if url[:url.index('#')] in self.visited:
                        continue
                except:
                    pass
                
                if url in self.visited:
                    continue
                else:
                    pass
                self.count = self.count+ 1
                print 'Having process', self.count , 'Pages'
                scraper = self.worker_class(url)
                self.visited.add(url)
                urlset, result_entity = scraper.execute()
                for i in urlset[0]:
                    #self.task_queue.put(i)
                    self.result_urls_queue.put(i)
                
                if result_entity != None:
                    pass
                else:
                    self.result_elements_queue.put(result_entity)
                    
            except:
                pass            
            finally:
                pass        
    def _worker(self):
        if self.all_dead != False:
            self.all_dead = False
        scraper = None
        while not self.all_dead:
            try:
                
                url = self.task_queue.get(block=True)
                print 'Workding', url
                try:
                    if url[:url.index('#')] in self.visited:
                        continue
                except:
                    pass
                
                if url in self.visited:
                    continue
                else:
                    pass
                self.count = self.count + 1
                print 'Having process', self.count , 'Pages'
                scraper = self.worker_class(url)
                self.visited.add(url)
                urlset, result_entity = scraper.execute()
                for i in urlset[0]:
                    if i in self.visited:
                        continue
                    else:
                        pass
                    self.task_queue.put(i)
                    self.result_urls_queue.put(i)
                
                if result_entity != None:
                    pass
                else:
                    self.result_elements_queue.put(result_entity)
                    
            except:
                pass            
            finally:
                pass
            

    """scraper interface"""
    def kill_workers(self):
        if self.all_dead == False:
            self.all_dead = True
        else:
            pass
    def feed(self, target_urls = []):
        if isinstance(target_urls, list):
            for target_url in target_urls:
                self.task_queue.put(target_url)
        elif isinstance(target_urls, str):
            self.task_queue.put(target_urls)
        else:
            pass
        
        
        #return url result
        return (self.get_result_urls_queue(), self.get_result_elements_queue() )
        