# coding=utf-8
import io
import sys

import requests

sys.path.append("../../../../")

from src.core.spider.enums import HTTP_CONTENT_TYPE




def get_file_from_url(title, url_file):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}
    req = requests.get(url_file, headers=send_headers)  # 通过访问互联网得到文件内容
    content_type = req.headers.get('Content-Type')

    if content_type.__contains__(HTTP_CONTENT_TYPE.HTML.value):
        # print(req.text)
        return req.text

    bytes_io = io.BytesIO(req.content)  # 转换为字节流
    with open(title + '.pdf', 'wb') as file:
        file.write(bytes_io.getvalue())  # 保存到本地
    # import time
    # time.sleep(2) # 最好做一个休眠
    return bytes_io


if __name__ == "__main__":
    # url = "https://sci.bban.top/pdf/10.1093/hmg/8.8.1517.pdf"
    url = 'https://moscow.sci-hub.st/3743/8ed96cf03594a185b637534dfaa2d160/devilliers1999.pdf#navpanes=0&view=FitH'
    # url = 'https://academic.oup.com/hmg/article-pdf/8/8/1517/1656473/8-8-1517.pdf' //moscow.sci-hub.st/3743/8ed96cf03594a185b637534dfaa2d160/devilliers1999.pdf#navpanes=0&view=FitH
    html = get_file_from_url('information', url)
    # bs = BeautifulSoup(html, 'html.parser')
    # title = bs.find(id='pdf')['src']

    # print(title)
