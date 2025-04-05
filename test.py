import sys
import time
from datetime import datetime

from src.common.dto.articledto.new_article import Article
from src.common.util.json_util import parseArticleToJsonStr
from src.core.annotate.service.annotate import Annotate
from src.core.annotate.service.annotator_singleton import get_shared_annotator
from src.core.render.service.RenderServiceImp import RenderServiceImp
from src.core.render.test.render_test import RenderController
from src.core.spider.service.article_analysis_service import ArticleAnalysisService
# from src.core.spider.service.article_analysis_service import ArticleAnalysisService
from src.core.spider.service.article_spider_service import ArticleSpiderService
from src.common.db.entity.article_entity import ArticleEntity


def process_article(pmc_id: str):
    # 查询指定pmc_id的文章
    article_entity = ArticleEntity.query(['*'], filter=[ArticleEntity.pmc_id == pmc_id], query_first=True,
                                         order_by='create_time')

    if article_entity is None:
        print(f"未能找到pmc_id为{pmc_id}的文章，程序退出")
        return

    print(f'文章转换开始：{article_entity.pmc_id}')
    ArticleEntity.update({'state': 1, 'start_time': datetime.now()}, [ArticleEntity.id == article_entity.id])

    # 初始化文章对象
    article = Article(articleEntity=article_entity)
    print(f'爬虫阶段开始：{article_entity.pmc_id}')
    ArticleSpiderService().crawl_article(article)
    print(f'解析阶段开始：{article_entity.pmc_id}')
    ArticleEntity.update({'state': 2}, [ArticleEntity.id == article_entity.id])
    ArticleAnalysisService(article).parsePdfFileToArticle()

    print(f'注释阶段开始：{article_entity.pmc_id}')
    article = get_shared_annotator().annotate(article)  # 对文章进行注释
    ArticleEntity.update({'state': 3, 'article_json': parseArticleToJsonStr(article), 'end_time': datetime.now()},
                         [ArticleEntity.id == article_entity.id])

    # 注释阶段之后的逻辑暂时注释掉
    print(f'渲染阶段开始：{article_entity.pmc_id}')
    ArticleEntity.update({'state': 4}, [ArticleEntity.id == article_entity.id])
    controller = RenderController(RenderServiceImp())  # 创建RenderController实例并注入RenderServiceImp实例
    controller.render_article(article)
    ArticleEntity.update(
        {'state': 5, 'article_json': parseArticleToJsonStr(article), 'end_time': datetime.now(), 'html_url':
            article.html_url},
        [ArticleEntity.id == article_entity.id])

    print(f'文章注释结束：{article_entity.pmc_id}')

if __name__ == "__main__":
    # 从命令行参数中获取pmc_id
    if len(sys.argv) < 2:
        print("请提供要处理的pmc_id作为命令行参数：python test.py [pmc_id]")
        sys.exit(1)

    pmc_id_to_process = sys.argv[1]  # 获取第一个命令行参数作为pmc_id
    process_article(pmc_id_to_process)
