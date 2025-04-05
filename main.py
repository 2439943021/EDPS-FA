# coding=utf-8
import time
from datetime import datetime

from src.common.db.entity.article_entity import ArticleEntity
from src.common.dto.articledto.new_article import Article
from src.common.util.json_util import parseArticleToJsonStr
from src.core.annotate.service.annotate import Annotate
from src.core.annotate.service.annotator_singleton import get_shared_annotator
from src.core.render.service.RenderServiceImp import RenderServiceImp
from src.core.render.test.render_test import RenderController
from src.core.spider.service.article_analysis_service import ArticleAnalysisService
# from src.core.spider.service.article_analysis_service import ArticleAnalysisService
from src.core.spider.service.article_spider_service import ArticleSpiderService


def searchArticle():
    articleEntity = ArticleEntity.query(['*'], filter=[ArticleEntity.state == "0"], query_first=True,
                                        order_by='create_time')
    if articleEntity is None:
        return
    print('文章转换开始' + articleEntity.pmc_id)
    ArticleEntity.update({'state': 1, 'start_time': datetime.now()}, [ArticleEntity.id == articleEntity.id])

    # 初始化文章
    article = Article(article_entity=articleEntity)
    print('爬虫阶段开始' + articleEntity.pmc_id)
    ArticleSpiderService().crawl_article(article)
    print('解析阶段开始' + articleEntity.pmc_id)
    ArticleEntity.update({'state': 2}, [ArticleEntity.id == articleEntity.id])
    ArticleAnalysisService(article).parse_pdf_file_to_article()

    print('注释阶段开始' + articleEntity.pmc_id)
    ArticleEntity.update({'state': 3}, [ArticleEntity.id == articleEntity.id])
    article = get_shared_annotator().annotate(article)  # 对文章进行注释

    print('渲染阶段开始' + articleEntity.pmc_id)
    ArticleEntity.update({'state': 4}, [ArticleEntity.id == articleEntity.id])
    controller = RenderController(RenderServiceImp())  # 创建RenderController实例并注入RenderServiceImp实例
    controller.render_article(article)
    ArticleEntity.update(
        {'state': 5, 'article_json': parseArticleToJsonStr(article), 'end_time': datetime.now(), 'html_url':
            article.html_url},
        [ArticleEntity.id == articleEntity.id])
    print('文章转换结束' + articleEntity.pmc_id)





def start():
    # ArticleSpiderService().start()
    ArticleAnalysisService().start()


if __name__ == "__main__":


    # start()
    count = 7
    while True:
        if count > 6:
            print('文章搜索中')
            count = 0
        else:
            count += 1
        try:
            searchArticle()
        except Exception as e:
            print(e)
        time.sleep(10)

    # UA伪装
    # service = ArticleSpiderService()
    # # 20727515
    # article = service.crawl_article('20727515')
    #
    # article = Annotate().annotate(article)  # 对文章进行注释
    # # article = parseJsonToArticleNode("../../../../src/common/util/output.json")
    # service = RenderServiceImp()  # 创建RenderServiceImp实例
    # controller = RenderController(RenderServiceImp())  # 创建RenderController实例并注入RenderServiceImp实例
    # controller.render_article(article)  # 调用RenderController实例的render_article方法渲染文章
    # articleAnalysisService = ArticleAnalysisService()
    # articleAnalysisService.parsePdfFileToArticle(
    #     './pdfs/20727515_TBC1D24,_an_ARF6-interacting_protein,_is_mutated_in_familial_infantile_myoclonic_epilepsy.pdf',
    #     SpiderConstants.PDF_ROOT_FLODER_PATH)
