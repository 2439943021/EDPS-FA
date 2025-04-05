# coding=utf-8
from src.common.log import logger_config
from src.core.spider.service.article_analysis_service import ArticleAnalysisService
from src.common.log import logger_config

if __name__ == "__main__":
    ArticleAnalysisService().start()