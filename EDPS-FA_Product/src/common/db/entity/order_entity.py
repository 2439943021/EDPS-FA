from sqlalchemy import String, Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from src.common.db.entity.base_entity import BaseEntity

# 创建Base类
Base = declarative_base()


# 创建ORM模型类
class ArticleEntity(Base, BaseEntity):
    __tablename__ = 'ask_user_orders'
    id = Column(String, primary_key=True)
    pmc_id = Column(String)
    post_id = Column(String)
    submit_type = Column(String)
    user_name = Column(String)
    user_id = Column(String)
    state = Column(String)
    visible = Column(String)
    create_time = Column(DateTime)
    end_time = Column(DateTime)


