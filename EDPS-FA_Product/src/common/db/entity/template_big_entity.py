from sqlalchemy import String, Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from src.common.db.entity.base_entity import BaseEntity

# 创建Base类
Base = declarative_base()


# 创建ORM模型类
class TemplateBig(Base, BaseEntity):
    __tablename__ = 'template_big'
    id = Column(String, primary_key=True)
    json_data = Column(Text)
    user_id = Column(String)
