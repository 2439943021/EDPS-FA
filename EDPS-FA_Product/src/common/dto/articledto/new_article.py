# coding=utf-8
from enum import Enum
from typing import Dict, Optional, Union
from dataclasses import dataclass, field
import uuid

from src.core.spider.entity.pubmed_entity import PubmedEntity


# 文章
class Article:
    def __init__(self, pubmed_entity=None, article_node=None, figures=None, article_entity=None, statistic_map=None,
                 entity_info_map=None, article_index_node=None, entity_type_color=None, entity_export_map=None):
        self.pubmed_entity = pubmed_entity
        self.article_node = article_node
        self.article_entity = article_entity
        self.html_path = ''
        self.html_url = ''
        self.excel_path = ''
        self.excel_url = ''
        self.zip_path = ''
        self.zip_url = ''
        if figures is None:
            figures = []
        # 图片
        self.figures = figures
        if statistic_map is None:
            statistic_map = StatisticMap()
        self.statistic_map = statistic_map
        # 如果entityInfoMap未定义，则创建一个新的EntityInfoMap实例
        if entity_info_map is None:
            entity_info_map = EntityInfoMap()
        if entity_export_map is None:
            entity_export_map = EntityExportMap()
        self.entity_info_map = entity_info_map
        self.entity_export_map = entity_export_map
        self.article_index_node = article_index_node
        self.entity_type_color = entity_type_color

    def to_dict(self):
        # 将Article对象转换为字典
        article_dict = {
            "figures": [figure.to_dict() for figure in self.figures],
        }
        if self.entity_info_map is not None:
            article_dict["entityInfoMap"] = self.entity_info_map.to_dict()
        if self.entity_export_map is not None:
            article_dict["entityExportMap"] = self.entity_export_map.to_dict()
        if self.statistic_map is not None:
            article_dict["statisticMap"] = self.statistic_map.to_dict()
        if self.article_node is not None:
            article_dict["articleNode"] = self.article_node.to_dict()
        if self.pubmed_entity is None:
            article_dict["pubmed_entity"] = None
        else:
            article_dict["pubmed_entity"] = self.pubmed_entity.to_dict()
        return article_dict

    @staticmethod
    def dict_to_article(articleDict):
        article = Article()
        if 'entityInfoMap' in articleDict:
            entity_info_map = EntityInfoMap.dict_to_entityInfoMap(articleDict['entityInfoMap'])
            article.entity_info_map = entity_info_map
        if 'entityExportMap' in articleDict:
            entity_export_map = EntityExportMap.dict_to_entityExportMap(articleDict['entityExportMap'])
            article.entity_export_map = entity_export_map
        if 'statisticMap' in articleDict:
            statistic_map = StatisticMap.dict_to_statisticMap(articleDict['statisticMap'])
            article.statistic_map = statistic_map
        if 'pubmed_entity' in articleDict:
            pubmed_entity = PubmedEntity.dict_to_entity(articleDict['pubmed_entity'])
            article.pubmed_entity = pubmed_entity
        if 'figures' in articleDict:
            figures_list = articleDict['figures']
            new_figure_list = []
            for figure in figures_list:
                new_figure_list.append(Figure.dict_to_figure(figure))
            article.figures = new_figure_list
        if 'articleNode' in articleDict:
            article_node = ArticleNode.dict_toNode(articleDict['articleNode'])
            article.article_node = article_node
        return article

    def traverse_nodes(self):
        yield self.article_node
        for node in self.article_node.nodes:
            yield from node.traverse_nodes()


class ArticleNode:
    def __init__(self, nodeType=None, content='', index=None, entities=None, nodes=None, fontSize=0):
        """
        文章节点
        @param nodeType:节点类型
        @param content: 节点内容
        @param index: 节点索引
        @param entities: 节点实体
        @param nodes:子节点
        """
        if nodes is None:
            nodes = []
        self.content = content
        self.nodeType = nodeType
        self.index = index
        if entities is None:
            entities = []
        self.entities = entities
        self.nodes = nodes
        # 字体大小，根据字体大小来划分段落
        self.fontSize = fontSize

    def put(self, node):
        """
        添加节点
        @param node:
        """
        self.nodes.append(node)

    def to_dict(self):
        # 将Article对象转换为字典
        article_node_dict = {
            "index": self.index,
            "content": self.content,
            "nodeType": self.nodeType.name,
            "fontSize": self.fontSize,
            "nodes": [node.to_dict() for node in self.nodes],
            "entities": [entity.to_dict() for entity in self.entities]
        }
        return article_node_dict

    @staticmethod
    def dict_toNode(dict):
        articleNode = ArticleNode()
        articleNode.index = dict['index']
        articleNode.content = dict['content']
        articleNode.nodeType = ArticleNodeType.convert_to_enum(dict['nodeType'])
        if 'entities' in dict:
            entities = dict['entities']
            for entity in entities:
                articleNode.entities.append(ArticleCardEntity.from_dict(entity))

        nodes = dict['nodes']
        for node in nodes:
            articleNode.put(ArticleNode.dict_toNode(node))

        # print("articleNode.entities:", dict('entities'))
        return articleNode

    def traverse_nodes(self):
        yield self
        for node in self.nodes:
            yield from node.traverse_nodes()


# 文章节点类型枚举
class ArticleNodeType(Enum):
    # 根节点
    ROOT = 0,
    # 标题
    TITLE = 1,
    # 段落
    PARAGRAPH = 2,
    # 句子
    SENTENCE = 3,

    def convert_to_enum(typeName):
        for nodeType in ArticleNodeType:
            if typeName == nodeType.name:
                return nodeType
        raise ValueError('Invalid ArticleNodeType')


class Figure:
    def __init__(self, content='', url='', index='', entities=[]):
        self.content = content  # 图题内容
        self.url = url  # 获取地址
        self.index = index  # 位置索引
        self.entities = entities

    def to_dict(self):
        # 将Entity对象转换为字典
        figure_dict = {
            "content": self.content,
            "url": self.url,
            "index": self.index,
            "entities": [entity.to_dict() for entity in self.entities]
        }
        return figure_dict

    @staticmethod
    def dict_to_figure(figureDict):
        figure = Figure()
        figure.index = figureDict['index']
        figure.url = figureDict['url']
        figure.content = figureDict['content']
        return figure


# 实体
# 使用 @dataclass 装饰器来标记实体类，并设置参数
@dataclass(order=True, frozen=True)
class ArticleCardEntity:
    # 定义实体的属性，并添加类型注解和默认值
    id: Optional[str] = field(default_factory=lambda: uuid.uuid4().hex, compare=False)
    name: Optional[str] = None
    type: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    info: Optional[Dict[str, str]] = None

    @staticmethod
    def from_dict(entity_dict: Dict[str, Union[str, int, Dict[str, str]]]) -> 'ArticleCardEntity':
        return ArticleCardEntity(
            id=entity_dict.get('id', uuid.uuid4().hex),
            name=entity_dict['name'],
            type=entity_dict['type'],
            start=entity_dict.get('start'),
            end=entity_dict.get('end'),
            info=entity_dict.get('info', {})
        )

    # 定义一个转换为字典的方法，并添加类型注解
    def to_dict(self):
        entity_dict = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "start": self.start,
            "end": self.end,
            "info": self.info,
        }
        return entity_dict


class StatisticMap:
    def __init__(self):
        self.statistic_map = {}

    def add_entity(self, category, entity, count):
        if category in self.statistic_map:
            self.statistic_map[category][entity] = count
        else:
            self.statistic_map[category] = {entity: count}

        # Sort the entities in descending order
        self.statistic_map[category] = dict(
            sorted(self.statistic_map[category].items(), key=lambda item: item[1], reverse=True))

    def increment_entity_count(self, category, entity):
        if category in self.statistic_map and entity in self.statistic_map[category]:
            self.statistic_map[category][entity] += 1
        else:
            self.add_entity(category, entity, 1)

    def get_statistic_map(self):
        return self.statistic_map

    def to_dict(self):
        return self.statistic_map

    @staticmethod
    def dict_to_statisticMap(statisticMapDict):
        statisticMap = StatisticMap()
        statisticMap.statistic_map = statisticMapDict
        return statisticMap


class EntityInfoMap:
    def __init__(self):
        self.entity_info_map = {}

    def add_entity_info_map(self, info_map):
        self.entity_info_map.update(info_map)

    def add_entity_info(self, entity, info):
        if entity not in self.entity_info_map:
            self.entity_info_map[entity] = info

    def get_entity_info_map(self):
        return self.entity_info_map

    def to_dict(self):
        return self.entity_info_map

    @staticmethod
    def dict_to_entityInfoMap(entityInfoMapDict):
        entityInfoMap = EntityInfoMap()
        entityInfoMap.entity_info_map = entityInfoMapDict
        return entityInfoMap


# 文章索引结构
class ArticleIndexNode:
    def __init__(self, index, statistic_map):
        """
        文章索引结构
        @param index: 索引
        @param statistic_map: 统计数据集
        """
        self.index = index
        self.statistic_map = statistic_map
        self.children = []

    # 从叶子结点依次向上进行集合相加 聚合数据
    def calculate_statistic_map(self):
        if not self.children:
            # print("没有子节点了 目前为 %s:%s" % (self.index, self.statistic_map))
            return self.statistic_map

        total_statistic_map = self.statistic_map
        # print("目前为 %s:%s" % (self.index, total_statistic_map))
        for child in self.children:
            # print("child %s:%s" % (child.index, child.statistic_map))
            child_statistic_map = child.calculate_statistic_map()
            for key, value in child_statistic_map.items():
                # print("key %s:value %s " % (key, value))
                if key in total_statistic_map:
                    # print("key %s 在当前集合%s 中" % (key, total_statistic_map))
                    for k, v in value.items():
                        if k in total_statistic_map[key]:
                            total_statistic_map[key][k] += v
                        else:
                            total_statistic_map[key][k] = v
                    # print("集合相加之后为：", total_statistic_map)
                else:
                    # print("key %s 不在当前集合%s 中" % (key, total_statistic_map))
                    total_statistic_map[key] = value
        # print("当前集合为 %s:%s" % (self.index, total_statistic_map))
        return total_statistic_map

    # 通过索引查找
    def find_statistic_map(self, index):
        if self.index == index:
            return self.statistic_map
        for child in self.children:
            result = child.find_statistic_map(index)
            if result:
                return result
        return None

class EntityExportMap:
    def __init__(self):
        self.entity_export_map = {}

    def add_entity_export_info_map(self, export_map):
        self.entity_export_map.update(export_map)

    def add_entity_export_info(self, entity, info):
        if entity not in self.entity_export_map:
            self.entity_export_map[entity] = info

    def get_entity_export_info_map(self):
        return self.entity_export_map

    def to_dict(self):
        return self.entity_export_map

    @staticmethod
    def dict_to_entityExportMap(entityExportMapDict):
        entityExportMap = EntityExportMap()
        entityExportMap.entity_export_map = entityExportMapDict
        return entityExportMap

if __name__ == '__main__':
    print('Python')
