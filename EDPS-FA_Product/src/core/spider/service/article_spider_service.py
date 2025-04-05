import sys
import time
import traceback
from datetime import datetime

import unicodedata

from src.common.db.dao.article_entity_dao import ArticleEntityDao
from src.common.db.entity.article_entity import ArticleEntity
from src.common.dto.articledto.new_article import Article
from src.common.enums.article_enums import ARTICLE_STATE
from src.common.util.json_util import parseArticleToJsonStr
from src.common.util.oss_util import upload_file
from src.core.spider.entity.pubmed_entity import PubmedEntity
from src.core.spider.util.pdf_download_util import *
from loguru import logger

class ArticleSpiderService:
    def __init__(self):
        self.article_entity_dao = ArticleEntityDao()

    def search_spider_article(self):
        article_entity = None
        """
        搜索爬虫文章
        @return:
        """
        try:

            article_entity = self.article_entity_dao.query_article_by_state(ARTICLE_STATE.ARTICLE_SPIDER_READY.value)
            if article_entity is None:
                return

            status = self.article_entity_dao.update_article(
                {'state': ARTICLE_STATE.ARTICLE_SPIDER_BEGIN.value,
                 'start_time': datetime.now(),
                 'version': article_entity.version + 1},
                [ArticleEntity.id == article_entity.id,
                 ArticleEntity.version == article_entity.version])
            if status == 0:
                return

            logger.info('爬虫阶段开始' + article_entity.pmc_id)
            article = Article(article_entity=article_entity)
            self.crawl_article(article)
            if article.pubmed_entity.is_success:
                self.article_entity_dao.update_article(
                    {'state': ARTICLE_STATE.ARTICLE_ANALYSIS_READY.value,
                     'article_json': parseArticleToJsonStr(article),
                     'author': article.pubmed_entity.author_list[0],
                     'title': article.pubmed_entity.title,
                     'pdf_oss_url': article.pubmed_entity.pdf_oss_url,
                     'pdf_path': article.pubmed_entity.download_path,
                     'pdf_spider_url': article.pubmed_entity.download_url,
                     'pdf_pubmed_url': article.pubmed_entity.pdf_pubmed_url},
                    [ArticleEntity.id == article_entity.id])

                logger.info('爬虫阶段结束' + article_entity.pmc_id)
            else:
                self.article_entity_dao.update_article(
                    {'state': ARTICLE_STATE.ARTICLE_SPIDER_ERROR.value,
                     'article_json': parseArticleToJsonStr(article),
                     'info': article.pubmed_entity.info, 'author': article.pubmed_entity.author_list[0],
                     'title': article.pubmed_entity.title},
                    [ArticleEntity.id == article_entity.id])
                logger.info('爬虫阶段结束 下载失败' + article_entity.pmc_id)

        except Exception:
            import traceback
            exception_str = traceback.format_exc()
            logger.info('爬虫阶段结束异常' + article_entity.pmc_id + exception_str)

            if article_entity is not None:
                self.article_entity_dao.update_article(
                    {'state': ARTICLE_STATE.ARTICLE_SPIDER_ERROR.value,
                     'info': exception_str},
                    [ArticleEntity.id == article_entity.id])

    def start(self):
        """
        服务开启
        """
        count = 7
        while True:
            if count > 6:
                logger.info('爬虫搜索')
                count = 0
            else:
                count += 1

                self.search_spider_article()

            time.sleep(10)

    # 爬取文章结构
    def crawl_article(self, article):

        self.crawl_pdf(article)

        # parseArticleToJsonFile(article, 'output.json')
        # return article

    def crawl_pdf(self, article):
        """
        爬取pdf
        @param paper_id:
        """
        paper_id = article.article_entity.pmc_id
        logger.info('开始爬取论文信息' + paper_id)
        pubmed_entity = self.crawl_info(paper_id)
        logger.info('开始下载论文信息' + paper_id)
        article.pubmed_entity = self.download_article(pubmed_entity)

        # 如果下载成功 准备上传到oss
        if pubmed_entity.is_success:
            logger.info('将论文上传到oss' + paper_id)

            # 将日期格式化为 yyyyMMdd 格式
            title = pubmed_entity.title
            now = datetime.now()
            timestamp = now.strftime('%Y%m%d')
            if len(title) > 156:
                title = title[:156]
            article.pubmed_entity.pdf_oss_url = upload_file(pubmed_entity.download_path,
                                                            'pdf/' + timestamp + '/' + paper_id + '/' + paper_id + '.pdf')

        return pubmed_entity

    def crawl_info(self, paper_id):
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
            logger.info(paper_id)
            logger.info(title)
            # print(author_list)
            # print(abstract)
            # print(links_dict)
            # print(pmc_id)
            # print(doi_id)
            # print(free_label)
            pubmed_entity = PubmedEntity(paper_id=paper_id, title=title, author_list=author_list, abstract=abstract,
                                         free_label=free_label, links_dict=links_dict, doi_id=doi_id,
                                         pmc_id=pmc_id)
            pubmed_entity.pdf_pubmed_url = url
            return pubmed_entity

        except:
            pubmed_entity = PubmedEntity(paper_id=paper_id)
            pubmed_entity.is_success = False
            traceback.print_exc()  # 打印异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))  # 将异常信息转为字符串
            logger.exception(paper_id)
            logger.exception(error)
            logger.exception()
            pubmed_entity.info = error
            return pubmed_entity

    def download_article(self, pubmed):
        if not pubmed.is_success:
            return pubmed
        # free label 优先考虑 欧洲中心2个做 其它 sci hub？
        try:
            # if pubmed.free_label:
            # 下载pubmed 中心
            if DownLoadCenterType.PUBMED_CENTRAL.value in pubmed.links_dict:
                isSuccess, path = download_pubmed_central(pubmed)
                if isSuccess:
                    pubmed.download_type = DownLoadCenterType.PUBMED_CENTRAL.value
                    pubmed.download_path = path
                    return pubmed
            # 下载欧洲中心
            if DownLoadCenterType.EUROPE_PUBMED_CENTRAL.value in pubmed.links_dict:
                isSuccess, path = download_europe_pubmed_central(pubmed)
                if isSuccess:
                    pubmed.download_type = DownLoadCenterType.EUROPE_PUBMED_CENTRAL.value
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
            if DownLoadCenterType.HAL.value in pubmed.links_dict:
                isSuccess, path = download_hal(pubmed)
                if isSuccess:
                    pubmed.download_type = DownLoadCenterType.HAL.value
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
            logger.info(pubmed.paper_id)
            logger.info(error)
            logger.info()
            pubmed.info = error
            pubmed.is_success = False
            return pubmed
