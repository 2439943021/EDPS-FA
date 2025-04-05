# coding=utf-8
import urllib

import requests
import io
import os
import re

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context


from bs4 import BeautifulSoup

from src.core.spider.enums import HTTP_CONTENT_TYPE


def get_file_from_url(path_floder, name, url):
    """
    下载pdf文件
    @param path_floder:
    @param name:
    @param url:
    @return:
    """
    try:
        if not os.path.exists(path_floder):
            os.makedirs(path_floder)
        name = sanitize_filename(name)
        send_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8"}

        req = requests.get(url, headers=send_headers, verify=False)  # 通过访问互联网得到文件内容
        content_type = req.headers.get('Content-Type')
        path = path_floder + name + '.pdf'

        # 避免下载到html
        if content_type.__contains__(HTTP_CONTENT_TYPE.HTML.value):
            return False, ''

        bytes_io = io.BytesIO(req.content)  # 转换为字节流
        with open(path, 'wb') as file:
            file.write(bytes_io.getvalue())  # 保存到本地
        if os.path.exists(path):
            return True, path
        return False, ''
    except Exception as e:
        print(e)
        return False, ''


def http_get_text(url):
    """
    http get 获取文本内容
    @param url:
    @return:
    """
    # UA
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                  (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }

    response = requests.get(url=url, headers=headers)
    page_text = response.text
    return page_text


def get_redict_url(url):
    """
    获取跳转URL
    @param url:
    @return:
    """
    with urllib.request.urlopen(url) as response:
        final_url = response.geturl()
    print(final_url)
    return final_url


def sanitize_filename(filename):
    """
    过滤不规则文件名
    @param filename:
    @return:
    """
    # 首先将文件名中的空格和 "." 替换为 "_"
    filename = re.sub(r'[.\s]+', '_', filename.strip())
    # 去除文件名中的非规则字符
    filename = re.sub(r'[<>:"/\\|?*]+', '', filename)
    if len(filename) > 260:
        return filename[:255]
    return filename


if __name__ == '__main__':
    url = 'https://sci-hub.st/10.1093/hmg/8.8.1517'
    print(get_redict_url(url))
    html = http_get_text(url)
    bs = BeautifulSoup(html, 'html.parser')
    pdf_link = bs.find('li', {'class': 'toolbar-item item-pdf js-item-pdf'})
    print(pdf_link.a['href'])
    '/hmg/articledto-pdf/8/8/1517/1656473/8-8-1517.pdf'
    'https://academic.oup.com'
    'https://academic.oup.com/hmg/article-pdf/8/8/1517/1656473/8-8-1517.pdf'
    print(html)
