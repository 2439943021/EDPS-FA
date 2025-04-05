# coding=utf-8
import re
import sys
import time
import traceback

import requests
import unicodedata

from src.core.spider.entity.pubmed_entity import PubmedEntity
from src.core.spider.util.pdf_download_util import *


# region Step 1 采集信息

def crawl_infos(info_list):
    pubmed_list = []

    for info in info_list:
        pubmed_list.append(crawl_info(info))
        time.sleep(1)

    return pubmed_list


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
        print(author_list)
        print(abstract)
        print(links_dict)
        print(pmc_id)
        print(doi_id)
        print(free_label)
        print()
        pubmed_entity = PubmedEntity(paper_id, title, author_list, abstract, free_label, links_dict, doi_id, pmc_id)

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
def download_articles(pubmed_list):
    new_pubmed_list = []
    for pubmed in pubmed_list:
        new_pubmed_list.append(download_article(pubmed))

    return new_pubmed_list


def download_article(pubmed):
    if not pubmed.is_success:
        return pubmed
    # free label 优先考虑 欧洲中心2个做 其它 sci hub？

    if pubmed.free_label:
        # 下载欧洲中心
        if DownLoadCenterType.EUROPE_PUBMED_CENTRAL.value in pubmed.links_dict:
            is_success, path = download_europe_pubmed_central(pubmed)
            if is_success:
                pubmed.download_type = DownLoadCenterType.EUROPE_PUBMED_CENTRAL.value
                pubmed.download_path = path
                return pubmed
        # 下载pubmed 中心
        if DownLoadCenterType.PUBMED_CENTRAL.value in pubmed.links_dict:
            is_success, path = download_pubmed_central(pubmed)
            if is_success:
                pubmed.download_type = DownLoadCenterType.PUBMED_CENTRAL.value
                pubmed.download_path = path
                return pubmed
        # 下载book 中心
        if DownLoadCenterType.NCBI_BOOKSHELF.value in pubmed.links_dict:
            is_success, path = download_bookshelf(pubmed)
            if is_success:
                pubmed.download_type = DownLoadCenterType.NCBI_BOOKSHELF.value
                pubmed.download_path = path
                return pubmed
        if DownLoadCenterType.HIGHWIRE.value in pubmed.links_dict:
            is_success, path = download_highwire(pubmed)
            if is_success:
                pubmed.download_type = DownLoadCenterType.HIGHWIRE.value
                pubmed.download_path = path
                return pubmed
        if DownLoadCenterType.SILVERCHAIR_INFORMATION_SYSTEMS.value in pubmed.links_dict:
            is_success, path = download_information_science(pubmed)
            if is_success:
                pubmed.download_type = DownLoadCenterType.SILVERCHAIR_INFORMATION_SYSTEMS.value
                pubmed.download_path = path

                return pubmed

    if pubmed.doi_id is not None:
        is_success, path = download_sci_hub(pubmed)
        if is_success:
            pubmed.download_type = DownLoadCenterType.SCIHUB.value
            pubmed.download_path = path
            return pubmed
    pubmed.is_success = False

    pubmed.info = str(pubmed.free_label) + str(pubmed.doi_id) + 'sci hub not install'
    return pubmed


# endregion

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
    file_result = open(save_path, 'a+')
    file_result.write('Total Count: ' + str(len(pubmed_list)) + '\n')
    file_result.write('Free Count: ' + str(free_count) + '\n')
    file_result.write('Download Count: ' + str(download_count) + '\n')
    file_result.write('Error Count: ' + str(error_count) + '\n')
    file_result.write('\n')
    file_result.close()

    for pubmed in pubmed_list:
        try:
            file_result = open(save_path, 'a+')
            file_result.write('Paper Id: ' + pubmed.paper_id + '\n')
            file_result.write('Title: ' + pubmed.title + '\n')
            file_result.write('Authors: ' + ",".join(pubmed.author_list) + '\n')
            file_result.write('Abstract:\n' + str(pubmed.abstract) + '\n')
            file_result.write('doi_id: ' + str(pubmed.doi_id) + '\n')
            file_result.write('pmc_id: ' + str(pubmed.pmc_id) + '\n')
            file_result.write('Is Free: ' + str(pubmed.free_label) + '\n')
            file_result.write('Pdf is success: ' + str(pubmed.is_success) + '\n')
            if pubmed.is_success:
                file_result.write('download_type: ' + pubmed.download_type + '\n')
                file_result.write('download path: ' + pubmed.download_path + '\n')
            else:
                file_result.write('Error Info: ' + pubmed.info + '\n')
            file_result.write('\n')
        except:
            pass
        finally:
            file_result.close()


# 开始爬取
def start_crawl(path):
    info_list = []

    with open(path, 'r') as file:
        line = ' '
        while line:
            line = file.readline()
            info_list.append(line.strip())
            if len(info_list) == 100:
                break
    print(info_list)
    # Step1 采集信息
    start_time = time.perf_counter()
    pubmed_list = crawl_infos(info_list)
    end_time = time.perf_counter()
    print("Step 1 time is: ", end_time - start_time, "s")

    # Step2 下载文章
    start_time = time.perf_counter()
    pubmed_list = download_articles(pubmed_list)
    end_time = time.perf_counter()
    print("Step 2 time is: ", end_time - start_time, "s")

    # Step3 Save Info
    print('Setp 3 Save Info Total Cont' + str(len(pubmed_list)))
    save_result(pubmed_list)


if __name__ == "__main__":
    path = 'var_citations_uniq.txt'
    start_crawl(path)
