# coding=utf-8


# 爬虫相关常量
class SpiderConstants:
    PDF_ROOT_FLODER_PATH='./pdfs/'

# 数据中心相关常量
class DataCenterConstants:
    EUROPE_PUBMED_CENTRAL_URL_1 = 'https://europepmc.org/backend/ptpmcrender.fcgi?accid='
    EUROPE_PUBMED_CENTRAL_URL_2 = '&blobtype=pdf'
    PUBMED_CENTRAL_URL_1 = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
    PUBMED_CENTRAL_URL_2 = '/pdf/main.pdf'
    SCI_HUB_BBAN_URL_1 = 'https://sci.bban.top/pdf/'
    SCI_HUB_BBAN_URL_2 = '.pdf'
    SCI_HUB_ST_1= 'https://sci-hub.st/'
    SCI_HUB_ST_2 = 'https:'
    NCBI_BOOKSHELF_URL_1 = 'https://www.ncbi.nlm.nih.gov/books/'
    NCBI_BOOKSHELF_URL_2 = '/pdf/Bookshelf_'
    NCBI_BOOKSHELF_URL_3 = '.pdf'
    HIGHWIRE_OLD = 'long'
    HIGHWIRE_NEW = 'full-text.pdf'
    SILVERCHAIR_INFORMATION_SYSTEMS = 'https://academic.oup.com'

    @staticmethod
    def EUROPE_PUBMED_CENTRAL_URL(pmc_id):
        return DataCenterConstants.EUROPE_PUBMED_CENTRAL_URL_1 + pmc_id + DataCenterConstants.EUROPE_PUBMED_CENTRAL_URL_2

    @staticmethod
    def PUBMED_CENTRAL_URL(pmc_id):
        return DataCenterConstants.PUBMED_CENTRAL_URL_1 + pmc_id + DataCenterConstants.PUBMED_CENTRAL_URL_2

    @staticmethod
    def SCI_HUB_BBAN_URL(doi_id):
        return DataCenterConstants.SCI_HUB_BBAN_URL_1 + doi_id + DataCenterConstants.SCI_HUB_BBAN_URL_2

    @staticmethod
    def SCI_HUB_ST_URL_1(doi_id):
        return DataCenterConstants.SCI_HUB_ST_1 + doi_id

    @staticmethod
    def SCI_HUB_ST_URL_2(url):
        return DataCenterConstants.SCI_HUB_ST_2 + url

    @staticmethod
    def NCBI_BOOKSHELF_URL(paper_id):
        return DataCenterConstants.NCBI_BOOKSHELF_URL_1 + paper_id + DataCenterConstants.NCBI_BOOKSHELF_URL_2 + paper_id + DataCenterConstants.NCBI_BOOKSHELF_URL_3

    @staticmethod
    def SILVERCHAIR_INFORMATION_SYSTEMS_URL(url):
        return DataCenterConstants.SILVERCHAIR_INFORMATION_SYSTEMS + url


if __name__ == '__main__':
    print('Python')
