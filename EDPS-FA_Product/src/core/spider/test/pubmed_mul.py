# coding=utf-8
import math
import sys
import threading
import time

import unicodedata
from bs4 import BeautifulSoup
import traceback, sys
from queue import Queue

import unicodedata

from src.core.spider.entity.pubmed_entity import PubmedEntity
from src.core.spider.util.pdf_download_util import *

# region 多线程 Config
from src.core.spider.enums import DownLoadCenterType

pubmed_queue = Queue()
MAX_CRAWL_THREADS = 10

res_pubmed_queue = Queue()
MAX_DOWNLOAD_THREADS = 15


# endregion


# region Step 1 采集信息

# 采集信息多线程
class CrawlInfoThread(threading.Thread):
    '''
    抓取线程类，注意需要继承线程类Thread
    '''

    def __init__(self, thread_id, queue):
        threading.Thread.__init__(self)  # 需要对父类的构造函数进行初始化
        self.thread_id = thread_id
        self.queue = queue  # 任务队列

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
                pubmed = crawl_info(paper_id)
                pubmed_queue.put(pubmed)


def crawl_infos(info_list):
    paper_id_queue = Queue()
    for info in info_list:
        paper_id_queue.put(info)
    #     pubmed_list.append(crawl_info(info))
    #     time.sleep(1)
    crawl_threads = []
    for i in range(MAX_CRAWL_THREADS):
        thread = CrawlInfoThread(i, paper_id_queue)  # 启动爬虫线程
        thread.start()  # 启动线程
        crawl_threads.append(thread)

    t1 = time.time()

    count = 1
    # 等待队列情况
    while not paper_id_queue.empty():  # 判断是否为空
        # pass  # 不为空，则继续阻塞
        count += 1
        if count > 1000:
            count = 1
            t2 = time.time()
            ftime = t2 - t1
            # 最多 10分钟一批
            if ftime > 600:
                break
    t2 = time.time()
    ftime = t2 - t1
    print('crawl_info_time', ftime)
    # 等待所有线程结束 队列为空后 最多100s
    limit_out = 20
    for t in crawl_threads:
        t.join(limit_out)

    return pubmed_queue


def crawl_info(paper_id):
    try:
        # UA
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }

        url = 'https://pubmed.ncbi.nlm.nih.gov/' + paper_id + '/'
        response = requests.get(url=url, headers=headers)
        page_text = response.text

        # html = urlopen('https://pubmed.ncbi.nlm.nih.gov/28263302/')
        # html = html.read()
        bs = BeautifulSoup(page_text, 'html.parser')
        title = bs.h1.text.replace("\n", '').strip()

        authors = bs.find_all('span', {'class': 'authors-list-item'})
        # 发送请求
        response = requests.get(url=url, headers=headers)
        author_list = []
        for author in authors:
            s = author.text
            s = s.replace(",", '').strip()
            s = re.sub(r'\s+', ' ', s)
            s = re.sub(r'[0-9]', ' ', s)
            s = unicodedata.normalize('NFKC', s).strip()
            author_list.append(s)

        abstract = bs.find('div', {'class': 'abstract-content selected'})
        if abstract is not None:
            abstract = re.sub(r'\s+', ' ', abstract.text.strip())
        else:
            abstract = 'Not Abstract'

        links = bs.find(class_='linkout-category-links')
        links_dict = {}
        if links is not None:
            for content in links.contents:
                text = content.text.replace('\n', '').strip()
                links_dict[text] = content.a['href']

        free_label = bs.find(class_='free-label')

        if free_label is not None:
            free_label = True
        else:
            free_label = False

        pmc_id = bs.find(class_='identifier pmc')

        if pmc_id is not None:
            pmc_id = pmc_id.a.text.strip()

        doi_id = bs.find(class_='identifier doi')
        if doi_id is not None:
            doi_id = doi_id.a.text.strip()
        print(paper_id)
        print(title)
        # print(author_list)
        # print(abstract)
        # print(links_dict)
        # print(pmc_id)
        # print(doi_id)
        # print(free_label)
        print()
        pubmed_entity = PubmedEntity(paper_id=paper_id, title=title, author_list=author_list, abstract=abstract,
                                     free_label=free_label, links_dict=links_dict, doi_id=doi_id, pmc_id=pmc_id)
        return pubmed_entity
    except:
        pubmed_entity = PubmedEntity(paper_id)
        pubmed_entity.is_success = False
        traceback.print_exc()  # 打印异常信息
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))  # 将异常信息转为字符串
        print(paper_id)
        print(error)
        print()
        pubmed_entity.info = error
        return pubmed_entity


# endregion

# region Step 2 下载文章

# 下载文章多线程
class DownloadThread(threading.Thread):
    '''
    抓取线程类，注意需要继承线程类Thread
    '''

    def __init__(self, thread_id, queue):
        threading.Thread.__init__(self)  # 需要对父类的构造函数进行初始化
        self.thread_id = thread_id
        self.queue = queue  # 任务队列

    def run(self):
        '''
        线程在调用过程中就会调用对应的run方法
        :return:
        '''
        print('启动线程：', self.thread_id)
        self.crawl_spider()
        print('退出了该线程：', self.thread_id)

    def crawl_spider(self):
        while True:
            if self.queue.empty():  # 如果队列为空，则跳出
                break
            else:
                pubmed = self.queue.get()
                print('当前工作的线程为：', self.thread_id, " 正在下载：", pubmed.paper_id)
                pubmed = download_article(pubmed)
                res_pubmed_queue.put(pubmed)


def download_articles(pubmed_queue):
    new_pubmed_list = []

    crawl_threads = []
    for i in range(MAX_CRAWL_THREADS):
        thread = DownloadThread(i, pubmed_queue)  # 启动爬虫线程
        thread.start()  # 启动线程
        crawl_threads.append(thread)

    # 等待队列情况
    t1 = time.time()

    count = 1
    while not pubmed_queue.empty():  # 判断是否为空
        # pass  # 不为空，则继续阻塞
        count += 1
        if count > 1000:
            count = 1
            t2 = time.time()
            ftime = t2 - t1
            # 最多 10分钟一批
            if ftime > 600:
                break

    t2 = time.time()
    ftime = t2 - t1
    print('download_article_time', ftime)
    # 等待所有线程结束

    limit_out = 20

    for t in crawl_threads:
        t.join(limit_out)

    while not res_pubmed_queue.empty():
        new_pubmed_list.append(res_pubmed_queue.get())

    # for pubmed in pubmed_list:
    #     new_pubmed_list.append(download_article(pubmed))

    return new_pubmed_list


def download_article(pubmed):
    if not pubmed.is_success:
        return pubmed
    # free label 优先考虑 欧洲中心2个做 其它 sci hub？
    try:
        if pubmed.free_label:
            # 下载欧洲中心
            if DownLoadCenterType.EUROPE_PUBMED_CENTRAL.value in pubmed.links_dict:
                isSuccess, path = download_europe_pubmed_central(pubmed)
                if isSuccess:
                    pubmed.download_type = DownLoadCenterType.EUROPE_PUBMED_CENTRAL.value
                    pubmed.download_path = path
                    return pubmed
            # 下载pubmed 中心
            if DownLoadCenterType.PUBMED_CENTRAL.value in pubmed.links_dict:
                isSuccess, path = download_pubmed_central(pubmed)
                if isSuccess:
                    pubmed.download_type = DownLoadCenterType.PUBMED_CENTRAL.value
                    pubmed.download_path = path
                    return pubmed
            # 下载book 中心
            if DownLoadCenterType.NCBI_BOOKSHELF.value in pubmed.links_dict:
                isSuccess, path = download_bookshelf(pubmed)
                if isSuccess:
                    pubmed.download_type = DownLoadCenterType.NCBI_BOOKSHELF.value
                    pubmed.download_path = path
                    return pubmed
            if DownLoadCenterType.HIGHWIRE.value in pubmed.links_dict:
                isSuccess, path = download_highwire(pubmed)
                if isSuccess:
                    pubmed.download_type = DownLoadCenterType.HIGHWIRE.value
                    pubmed.download_path = path
                    return pubmed
            if DownLoadCenterType.SILVERCHAIR_INFORMATION_SYSTEMS.value in pubmed.links_dict:
                isSuccess, path = download_information_science(pubmed)
                if isSuccess:
                    pubmed.download_type = DownLoadCenterType.SILVERCHAIR_INFORMATION_SYSTEMS.value
                    pubmed.download_path = path
                    return pubmed

        if pubmed.doi_id is not None:
            isSuccess, path = download_sci_hub(pubmed)
            if isSuccess:
                pubmed.download_type = DownLoadCenterType.SCIHUB.value
                pubmed.download_path = path
                return pubmed
        pubmed.is_success = False

        pubmed.info = str(pubmed.free_label) + str(pubmed.doi_id) + 'sci hub not install'
        return pubmed
    except:
        traceback.print_exc()  # 打印异常信息
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))  # 将异常信息转为字符串
        print(pubmed.paper_id)
        print(error)
        print()
        pubmed.info = error
        pubmed.is_success = False
        return pubmed


# endregion

# region Step3 保存结果
def save_result(pubmed_list):
    save_path = 'pubmed_info.txt'

    free_count, download_count, error_count = 0, 0, 0
    for pubmed in pubmed_list:
        if pubmed.is_success:
            download_count += 1
        else:
            error_count += 1
        if pubmed.free_label:
            free_count += 1
    fresult = open(save_path, 'a+')
    fresult.write('Total Count: ' + str(len(pubmed_list)) + '\n')
    fresult.write('Free Count: ' + str(free_count) + '\n')
    fresult.write('Download Count: ' + str(download_count) + '\n')
    fresult.write('Error Count: ' + str(error_count) + '\n')
    fresult.write('\n')
    fresult.close()

    for pubmed in pubmed_list:
        try:
            fresult = open(save_path, 'a+')
            fresult.write('Paper Id: ' + pubmed.paper_id + '\n')
            fresult.write('Title: ' + pubmed.title + '\n')
            fresult.write('Authors: ' + ",".join(pubmed.author_list) + '\n')
            fresult.write('Abstract:\n' + str(pubmed.abstract) + '\n')
            fresult.write('doi_id: ' + str(pubmed.doi_id) + '\n')
            fresult.write('pmc_id: ' + str(pubmed.pmc_id) + '\n')
            fresult.write('Is Free: ' + str(pubmed.free_label) + '\n')
            fresult.write('Pdf is success: ' + str(pubmed.is_success) + '\n')
            if pubmed.is_success:
                fresult.write('download_type: ' + pubmed.download_type + '\n')
                fresult.write('download path: ' + pubmed.download_path + '\n')
            else:
                fresult.write('Error Info: ' + pubmed.info + '\n')
            fresult.write('\n')
        except:
            pass
        finally:
            fresult.close()


# endregion


# 开始爬取
def start_crawl(path):
    info_list = []

    with open(path, 'r') as file:
        line = ' '
        while line:
            line = file.readline()
            info_list.append(line.strip())
    print(info_list)
    # Step1 采集信息
    start_time = time.perf_counter()
    pubmed_queue = crawl_infos(info_list)
    end_time = time.perf_counter()
    print("Step 1 time is: ", end_time - start_time, "s")

    # Step2 下载文章
    start_time = time.perf_counter()
    pubmed_list = download_articles(pubmed_queue)
    end_time = time.perf_counter()
    print("Step 2 time is: ", end_time - start_time, "s")

    # Step3 Save Info
    print('Setp 3 Save Info Total Cont' + str(len(pubmed_list)))
    save_result(pubmed_list)


# 开始爬取
def start_crawl_spilt(path):
    info_list = []

    with open(path, 'r') as file:
        line = ' '
        while line:
            line = file.readline()
            info_list.append(line.strip())
            # if len(info_list) == 500:
            #     break
    # 1000起做吧
    m = 100
    n = int(math.ceil(len(info_list) / float(m)))
    info_list = [info_list[i:i + n] for i in range(0, len(info_list), n)]
    for i in range(len(info_list)):
        print('Stage Start', i + 1)
        start_crawl_spilt_step(info_list[i])
        print('Stage End', i + 1)


def start_crawl_spilt_step(info_list):
    # Step1 采集信息
    start_time = time.perf_counter()
    pubmed_queue = crawl_infos(info_list)
    end_time = time.perf_counter()
    print("Step 1 time is: ", end_time - start_time, "s")

    # Step2 下载文章
    start_time = time.perf_counter()
    pubmed_list = download_articles(pubmed_queue)
    end_time = time.perf_counter()
    print("Step 2 time is: ", end_time - start_time, "s")

    # Step3 Save Info
    print('Setp 3 Save Info Total Cont' + str(len(pubmed_list)))
    save_result(pubmed_list)


if __name__ == "__main__":
    path = 'pmid-gainoffunc-set-20231214.txt'
    # start_crawl(path)

    start_crawl_spilt(path)
