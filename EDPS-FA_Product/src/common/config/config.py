# -*- coding: utf-8 -*-
# @Time    : 2024/4/23 9:45:46
# @Author  : kjh
# @File    : config.py
# @Software: PyCharm
import os


class Config:
    ENV = "QA"
    # rds配置信息
    DB_HOST = "127.0.0.1"
    DB_USER = "root"
    DB_PASSWORD = "123456"
    DB_PORT = 3306
    DB_NAME = "ask"
    DB_CHARSET = "utf8"

    # 开发环境渲染模块路径配置信息
    # 模板资源路径
    TEMPLATE_DIR = "../resource"
    TEMPLATE_FILE = "reconstruct_template.html"
    TEMPLATE_OUT_DIR = "temp_rendered_output.html"

    # 输出json资源路径
    OUTPUT_JSON_DIR = "../resource/json"
    OUTPUT_JSON_FILE = 'output.json'
    OUTPUT_ARTICLE_JSON_FILE = 'article.json'

    # 配置文件资源路径
    CONFIG_DIR = '../config'
    ENTITY_CATEGORY_DIR = 'entity_categories.yaml'

    # 模板动态模块资源路径
    MODULES_DIR = '../resource/modules'
    MIDDLE_BODY_FILE = '/middle/middle_body.html'
    RIGHT_NAVIGATOR_FILE = '/right/right_navigator.html'
    ENTITY_CATEGORY_DIR = '/outer/entityCard.html'


    #OSS通用
    OSS_QINIU_ACCESS_KEY = "6PgvXRaa550i0rb1eAeVqOcFRy1AxzMbVpYFFlQ7"
    OSS_QINIU_SECRET_KEY = "TIBscLPF-TQm2qn84WwtDpe1GEk1Q1lTOhcpN4BJ"
    OSS_QINIU_BUCKET_NAME = "medseeker-oss"
    OSS_QINIU_BUCKET_DOMAIN = "https://ask.longwend.com/"

    #爬虫PDF下载文件根路径 这边提供的是绝对路径 以适应不同的环境
    SPIDER_FOLDER_PATH= r'/home/jsj616/kjh/gg_test/pdfs/'

    RENDER_REPORT_DIR = "report/"



class DevConfig(Config):
    ENV = "DEV"
    # 开发环境rds配置信息
    DB_HOST = "rm-8vb7w4mo8b6npnet2go.mysql.zhangbei.rds.aliyuncs.com"
    DB_USER = "root"
    DB_PASSWORD = "LWcc123456"
    DB_PORT = 3306
    DB_NAME = "ask"
    DB_CHARSET = "utf8"

    # 开发环境爬虫模块路径配置信息

    # 开发环境解析模块路径配置信息

    # 开发环境识别模块路径配置信息

    # 开发环境渲染模块路径配置信息
    # 模板资源路径
    TEMPLATE_DIR = "../resource"
    TEMPLATE_FILE = "reconstruct_template.html"
    TEMPLATE_OUT_DIR = "temp_rendered_output.html"

    # 输出json资源路径
    OUTPUT_JSON_DIR = "../resource/json"
    OUTPUT_JSON_FILE = 'output.json'
    OUTPUT_ARTICLE_JSON_FILE = 'article.json'

    # 配置文件资源路径
    CONFIG_DIR = '../config'
    ENTITY_CATEGORY_DIR = 'entity_categories.yaml'

    # 模板动态模块资源路径
    MODULES_DIR = '../resource/modules'
    MIDDLE_BODY_FILE = '/middle/middle_body.html'
    RIGHT_NAVIGATOR_FILE = '/right/right_navigator.html'
    ENTITY_CATEGORY_DIR = '/outer/entityCard.html'

    # 输出报告路径
    RENDER_REPORT_DIR = '../resource/report'


class QAConfig(Config):
    ENV = "QA"
    # 测试环境rds配置信息
    DB_HOST = "rm-8vb7w4mo8b6npnet2go.mysql.zhangbei.rds.aliyuncs.com"
    DB_USER = "root"
    DB_PASSWORD = "LWcc123456"
    DB_PORT = 3306
    DB_NAME = "ask_test"
    DB_CHARSET = "utf8"

    # 生产环境七牛云oss配置信息
    OSS_QINIU_ACCESS_KEY = "6PgvXRaa550i0rb1eAeVqOcFRy1AxzMbVpYFFlQ7"
    OSS_QINIU_SECRET_KEY = "TIBscLPF-TQm2qn84WwtDpe1GEk1Q1lTOhcpN4BJ"
    OSS_QINIU_BUCKET_NAME = "medseeker-oss"
    OSS_QINIU_BUCKET_DOMAIN = "https://ask.genemed.tech/"

    # 生产环境爬虫模块路径配置信息
    SPIDER_FOLDER_PATH = r'/mnt/d/ask/Autovalseeker/pdfs/'

    # 生产环境解析模块路径配置信息

    # 生产环境识别模块路径配置信息

    # 生产环境渲染模块路径配置信息
    RENDER_REPORT_DIR = "report/"



class ProdConfig(Config):
    ENV = "PROD"
    # 生产环境rds配置信息
    DB_HOST = "rm-8vb7w4mo8b6npnet2go.mysql.zhangbei.rds.aliyuncs.com"
    DB_USER = "root"
    DB_PASSWORD = "LWcc123456"
    DB_PORT = 3306
    DB_NAME = "ask"
    DB_CHARSET = "utf8"

    # 生产环境七牛云oss配置信息
    OSS_QINIU_ACCESS_KEY = "6PgvXRaa550i0rb1eAeVqOcFRy1AxzMbVpYFFlQ7"
    OSS_QINIU_SECRET_KEY = "TIBscLPF-TQm2qn84WwtDpe1GEk1Q1lTOhcpN4BJ"
    OSS_QINIU_BUCKET_NAME = "medseeker-oss"
    OSS_QINIU_BUCKET_DOMAIN = "https://ask.genemed.tech/"

    # 生产环境爬虫模块路径配置信息
    SPIDER_FOLDER_PATH = r'/mnt/d/ask/Autovalseeker/pdfs/'

    # 生产环境解析模块路径配置信息

    # 生产环境识别模块路径配置信息

    # 生产环境渲染模块路径配置信息
    RENDER_REPORT_DIR = "report/"


mapping = {
    'dev': DevConfig,
    'qa': QAConfig,
    'prod': ProdConfig
}

APP_ENV = os.environ.get('APP_ENV', 'prod').lower()  # 需要手动修改此项切换环境
config = mapping[APP_ENV]()
"""
使用样例：
    from src.common.config.Config import config
    print(config.DB_HOST)
"""
if __name__ == '__main__':
    print(config.ENV)
    print(config.DB_HOST)
    print(config.DB_NAME)
