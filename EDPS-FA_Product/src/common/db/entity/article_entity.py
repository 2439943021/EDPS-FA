from sqlalchemy import String, Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from src.common.db.entity.base_entity import BaseEntity

# 创建Base类
Base = declarative_base()


# 创建ORM模型类
class ArticleEntity(Base, BaseEntity):
    __tablename__ = 'article'
    id = Column(String, primary_key=True)
    pmc_id = Column(String)
    state = Column(String)
    article_json = Column(Text)
    pdf_spider_url = Column(String)
    pdf_oss_url = Column(String)
    pdf_path = Column(String)
    pdf_pubmed_url = Column(String)
    html_url = Column(String)
    html_path = Column(String)
    excel_url = Column(String)
    excel_path = Column(String)
    zip_url = Column(String)
    zip_path = Column(String)
    title = Column(String)
    author = Column(String)
    user_id = Column(String)
    info = Column(Text)
    version = Column(Integer)
    create_time = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    update_time = Column(DateTime)
    entity_color_json = Column(Text)
    # 新增template_big_id
    template_big_id = Column(String)

