from enum import Enum


class ARTICLE_STATE(Enum):
    # 状态码 00 待开始 11指爬虫待开始 12爬虫开始  13爬虫失败 21解析待开始 22解析进行中 23解析失败  31识别待开始 32识别进行中 33识别失败 41渲染待开始 42渲染进行中 43 渲染失败 51完成
    ARTICLE_TO_BEGIN = '00'
    ARTICLE_OK = '51'
    ARTICLE_SPIDER_READY = '11'
    ARTICLE_SPIDER_BEGIN = '12'
    ARTICLE_SPIDER_ERROR = '13'
    ARTICLE_ANALYSIS_READY = '21'
    ARTICLE_ANALYSIS_BEGIN = '22'
    ARTICLE_ANALYSIS_ERROR = '23'
    ARTICLE_ANNOTATE_READY = '31'
    ARTICLE_ANNOTATE_BEGIN = '32'
    ARTICLE_ANNOTATE_ERROR = '33'
    ARTICLE_RENDER_READY = '41'
    ARTICLE_RENDER_BEGIN = '42'
    ARTICLE_RENDER_ERROR = '43'
