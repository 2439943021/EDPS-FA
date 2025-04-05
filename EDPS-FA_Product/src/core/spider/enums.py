# coding=utf-8

from enum import Enum


class DownLoadType(Enum):
    FAILED = (0, 'failed')
    FREE_DOWNLOAD = (1, 'free_download')
    SCI_HUB = (2, 'sci_hub')

    def __init__(self, code, info):
        self.code = code
        self.info = info

    def __str__(self):
        return self.code + self.info


class DownLoadCenterType(Enum):
    PUBMED_CENTRAL = 'PubMed Central'
    EUROPE_PUBMED_CENTRAL = 'Europe PubMed Central'
    ELSEVIER_SCIENCE = 'Elsevier Science'
    SILVERCHAIR_INFORMATION_SYSTEMS = 'Silverchair Information Systems'
    NCBI_BOOKSHELF = 'NCBI Bookshelf'
    HIGHWIRE = 'HighWire'
    SCIHUB = 'SCI-HUB'
    HAL = 'HAL archives ouvertes'


class HTTP_CONTENT_TYPE(Enum):
    HTML = 'text/html'
    PDF = 'application/pdf'


# 布局类型
class ParseLayoutType(Enum):
    TEXT = 'Text'
    FIGURE = 'Figure'
    TITLE = 'Title'
    TABLE = 'Table'
    LIST = 'List'


if __name__ == '__main__':
    print('Python')
