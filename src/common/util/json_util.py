import json

from src.common.dto.articledto.new_article import ArticleNode, ArticleNodeType, Article, Figure
from src.core.spider.entity.pubmed_entity import PubmedEntity


def parseArticleToJsonFile(article, path):
    """
    将文章结构转为Node
    @param articleNode:
    @param path:
    """
    str = article.to_dict()
    json_str = json.dumps(str)
    with open(path, "w") as file:
        json.dump(json_str, file)


def parseArticleToJsonStr(article):
    """
    将文章结构转为Json
    @param articleNode:
    """
    str = article.to_dict()
    jsonStr = json.dumps(str)
    return jsonStr


def parseJsonToArticleNode(path):
    """
    将json文件转为article对象
    @param path:
    """
    # 从JSON文件中读取数据
    with open(path, "r") as file:
        data = json.load(file)

    article = Article.dict_to_article(data)

    return article


def parse_json_str_to_article_node(jsonStr):
    """
    将json文件转为article对象
    @param path:
    """
    # 从JSON文件中读取数据
    data = json.loads(jsonStr)
    article = Article.dict_to_article(data)

    return article


if __name__ == "__main__":
    # tempNode = ArticleNode(index='1', nodeType=ArticleNodeType.SENTENCE, content="sentence",
    #                        fontSize=15)
    # parseArticleToJsonFile(tempNode,"output.json")
    parseJsonToArticleNode("output.json")
