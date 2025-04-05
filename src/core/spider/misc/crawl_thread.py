import threading


# 采集信息多线程
class CrawlInfoThread(threading.Thread):
    '''
    抓取线程类，注意需要继承线程类Thread
    '''

    def __init__(self, thread_id, queue,crawlService):
        threading.Thread.__init__(self)  # 需要对父类的构造函数进行初始化
        self.thread_id = thread_id
        self.queue = queue  # 任务队列
        self.crawlService=crawlService

    def run(self):
        '''
        线程在调用过程中就会调用对应的run方法
        :return:
        '''
        print('启动线程：', self.thread_id)
        self.crawl_spider()
        print('退出了该线程：', self.thread_id, '\n')

    def crawl_spider(self):
        while True:
            if self.queue.empty():  # 如果队列为空，则跳出
                break
            else:
                paper_id = self.queue.get()
                print('当前工作的线程为：', self.thread_id, " 正在采集：", paper_id)
                pubmed = self.crawlService.crawl_info(paper_id)
                pubmed_queue.put(pubmed)
