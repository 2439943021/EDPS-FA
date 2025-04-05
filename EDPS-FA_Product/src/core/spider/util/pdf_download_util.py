# coding=utf-8

from src.core.spider.util.http_util import *
from src.core.spider.constants import DataCenterConstants, SpiderConstants

from src.core.spider.enums import DownLoadCenterType
from bs4 import BeautifulSoup

from src.common.config.config import config

path_folder = config.SPIDER_FOLDER_PATH


def get_path_folder(pubmed_entity):
    """
    统一规整下载文件路径
    @param pubmed_entity:
    @return:
    """
    return path_folder + pubmed_entity.paper_id + '/'


def download_europe_pubmed_central(pubmed_entity):
    """
    下载欧洲中心pdf
    @param pubmed_entity:
    @return:
    """
    print(pubmed_entity.pmc_id)
    url = DataCenterConstants.EUROPE_PUBMED_CENTRAL_URL(pubmed_entity.pmc_id)
    pubmed_entity.download_url = url
    return get_file_from_url(get_path_folder(pubmed_entity), pubmed_entity.paper_id + '_' + pubmed_entity.title, url)


#
def download_pubmed_central(pubmed_entity):
    """
    下载pubmed中心pdf
    @param pubmed_entity:
    @return:
    """
    print(pubmed_entity.pmc_id)
    url = DataCenterConstants.PUBMED_CENTRAL_URL(pubmed_entity.pmc_id)
    pubmed_entity.download_url = url
    return get_file_from_url(get_path_folder(pubmed_entity), pubmed_entity.paper_id + '_' + pubmed_entity.title, url)


def download_sci_hub(pubmed_entity):
    """
    下载scihub pdf
    @param pubmed_entity:
    @return:
    """
    try:
        print(pubmed_entity.doi_id)
        url = DataCenterConstants.SCI_HUB_BBAN_URL(pubmed_entity.doi_id)
        pubmed_entity.download_url = url
        isSuccess, path = get_file_from_url(get_path_folder(pubmed_entity),
                                            pubmed_entity.paper_id + '_' + pubmed_entity.title, url)
        if isSuccess:
            return isSuccess, path
        else:
            print('SCI BAAN Can not download')
        url = DataCenterConstants.SCI_HUB_ST_URL_1(pubmed_entity.doi_id)
        html = http_get_text(url)
        bs = BeautifulSoup(html, 'html.parser')
        url = bs.find(id='pdf')['src']
        url = DataCenterConstants.SCI_HUB_ST_URL_2(url)
        return get_file_from_url(get_path_folder(pubmed_entity), pubmed_entity.paper_id + '_' + pubmed_entity.title, url)
    except Exception as e:
        print(e)
        return False, ''



def download_bookshelf(pubmed_entity):
    """
    下载ncbi book pdf
    @param pubmed_entity:
    @return:
    """
    print(pubmed_entity.paper_id)
    url = DataCenterConstants.NCBI_BOOKSHELF_URL(pubmed_entity.paper_id)
    pubmed_entity.download_url = url
    return get_file_from_url(get_path_folder(pubmed_entity), pubmed_entity.paper_id + '_' + pubmed_entity.title, url)


def download_highwire(pubmed_entity):
    """
    下载ncbi book pdf
    @param pubmed_entity:
    @return:
    """
    print(pubmed_entity.links_dict[DownLoadCenterType.HIGHWIRE.value])
    try:
        url = get_redict_url(pubmed_entity.links_dict[DownLoadCenterType.HIGHWIRE.value])
        pubmed_entity.download_url = url
        parts = url.rsplit(DataCenterConstants.HIGHWIRE_OLD, 1)
        if len(parts) > 1:
            url = parts[0] + DataCenterConstants.HIGHWIRE_NEW + parts[1][len(DataCenterConstants.HIGHWIRE_OLD):]
            pubmed_entity.download_url = url
            return get_file_from_url(get_path_folder(pubmed_entity), pubmed_entity.paper_id + '_' + pubmed_entity.title, url)
        else:
            return False, ''
    except Exception as e:
        print(e)
        return False, ''



def download_information_science(pubmed_entity):
    """
    下载information science
    @param pubmed_entity:
    @return:
    """
    print(pubmed_entity.links_dict[DownLoadCenterType.SILVERCHAIR_INFORMATION_SYSTEMS.value])
    try:
        url = get_redict_url(pubmed_entity.links_dict[DownLoadCenterType.SILVERCHAIR_INFORMATION_SYSTEMS.value])
        html = http_get_text(url)
        bs = BeautifulSoup(html, 'html.parser')
        pdf_link = bs.find('li', {'class': 'toolbar-item item-pdf js-item-pdf'})
        url = DataCenterConstants.SILVERCHAIR_INFORMATION_SYSTEMS_URL(pdf_link)
        pubmed_entity.download_url = url
        return get_file_from_url(get_path_folder(pubmed_entity), pubmed_entity.paper_id + '_' + pubmed_entity.title,
                                 url)
    except Exception as e:
        print(e)
        return False, ''

def download_hal(pubmed_entity):
    """
    下载HAL
    @param pubmed_entity:
    @return:
    """
    print(pubmed_entity.links_dict[DownLoadCenterType.HAL.value])
    try:
        # 获取html
        html = http_get_text(pubmed_entity.links_dict[DownLoadCenterType.HAL.value])
        bs = BeautifulSoup(html, 'html.parser')
        div_link = bs.find('div', {'class': 'section-content section-shadow hal-visualize-button widget-files'})
        first_link = div_link.find('a')
        url = first_link.get('href')
        pubmed_entity.download_url = url
        return get_file_from_url(get_path_folder(pubmed_entity), pubmed_entity.paper_id + '_' + pubmed_entity.title,
                                 url)
    except Exception as e:
        print(e)
        return False, ''

if __name__ == '__main__':
    print('Python')
