from sqlalchemy import String, Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from src.common.db.entity.base_entity import BaseEntity

# 创建Base类
Base = declarative_base()


# 创建ORM模型类
class TemplateSmall(Base, BaseEntity):
    __tablename__ = 'template_small'
    small_temp_id = Column(String, primary_key=True)
    small_temp_name = Column(String)
    temp_json = Column(Text)
    user_id = Column(String)

