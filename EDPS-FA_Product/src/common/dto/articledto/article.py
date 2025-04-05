# coding=utf-8
from typing import Dict, Optional
from dataclasses import dataclass, field
import uuid


# 文章
class Article:
    def __init__(self, pubmed_entity=None, articleEntity=None):
        self.pubmed_entity = pubmed_entity
        self.articleEntity = articleEntity
        # 全文
        self.content = ''
        # 标题
        self.title = []
        # 摘要
        self.abstract = []
        # 章节
        self.chapters = []
        # 图片
        self.figures = []

    def to_dict(self):
        # 将Article对象转换为字典
        article_dict = {
            "pubmed_entity": self.pubmed_entity.to_dict(),
            "content": self.content,
            "chapters": [chapter.to_dict() for chapter in self.chapters]
        }
        return article_dict


class Title:
    def __init__(self, content):
        self.content = content
        self.entitys = []


class Abstract:
    def __init__(self, content):
        self.content = content
        self.entitys = []


class Figure:
    def __init__(self, title, content, url, index=""):
        self.title = title  # 图题
        self.content = content  # 图题内容
        self.url = url  # 获取地址
        self.index = index  # 位置索引

    def to_dict(self):
        # 将Entity对象转换为字典
        figure_dict = {
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "index": self.index
        }
        return figure_dict


# 章节
class Chapter:
    def __init__(self, index, chapter_title, content):
        #  章节索引
        self.index = index
        # 章节标题
        self.chapter_title = chapter_title
        # 章节内容
        self.content = content
        # 段落
        self.paragraphs = []

    def to_dict(self):
        # 将Chapter对象转换为字典
        chapter_dict = {
            "index": self.index,
            "chapter_title": self.chapter_title,
            "content": self.content,
            "paragraphs": [paragraph.to_dict() for paragraph in self.paragraphs]
        }
        return chapter_dict


# 段落
class Paragraph:
    def __init__(self, index, sub_chapter_title, content):
        #  段落索引
        self.index = index
        # 章节小标题
        self.sub_chapter_title = sub_chapter_title
        # 段落内容
        self.content = content
        # 句子
        self.sentences = []

    def to_dict(self):
        # 将Paragraph对象转换为字典
        paragraph_dict = {
            "index": self.index,
            "sub_chapter_title": self.sub_chapter_title,
            "content": self.content,
            "sentences": [sentence.to_dict() for sentence in self.sentences]
        }
        return paragraph_dict


# 句子
class Sentence:
    def __init__(self, index, content):
        #  句子索引
        self.index = index
        #  句子内容
        self.content = content
        # TODO 存放句子信息的
        self.entitys = []

    def to_dict(self):
        # 将Sentence对象转换为字典
        sentence_dict = {
            "index": self.index,
            "content": self.content,
            "entity": [entity.to_dict() for entity in self.entitys]
        }
        return sentence_dict


# 实体
# 使用 @dataclass 装饰器来标记实体类，并设置参数
@dataclass(order=True, frozen=True)
class Entity:
    # 定义实体的属性，并添加类型注解和默认值
    id: Optional[str] = field(default_factory=lambda: uuid.uuid4().hex, compare=False)
    name: Optional[str] = None
    type: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    info: Optional[Dict[str, str]] = None

    # 定义一个转换为字典的方法，并添加类型注解
    def to_dict(self) -> Dict[str, str]:
        # 将Entity对象转换为字典
        entity_dict = {
            "name": self.name,
            "type": self.type,
            "start": self.start,
            "end": self.end
        }
        return entity_dict


class Info:
    def __init__(self):
        pass


if __name__ == '__main__':
    print('Python')
