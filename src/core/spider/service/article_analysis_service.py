import os
import sys
import time
from functools import cmp_to_key

import cv2
import layoutparser as lp
from sqlalchemy import column

from src.common.db.entity.article_entity import ArticleEntity
from src.common.dto.articledto.new_article import Article, Figure, ArticleNode, ArticleNodeType
from src.common.enums.article_enums import ARTICLE_STATE
from src.common.util.file_util import del_file
from src.common.util.json_util import parseArticleToJsonStr, parse_json_str_to_article_node
from src.core.spider.entity.pubmed_entity import PubmedEntity
from src.core.spider.enums import ParseLayoutType
from src.core.spider.util.content_util import split_sentences
from src.core.spider.util.pdf_util import convert_pdf_to_image
from src.common.util.oss_util import upload_file
from datetime import datetime

from src.common.db.dao.article_entity_dao import ArticleEntityDao


import resource
from pynvml import nvmlDeviceGetHandleByIndex, nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetMemoryInfo, nvmlDeviceGetName, \
    nvmlDeviceGetTemperature, nvmlShutdown
import gc

from PIL import Image
from src.core.spider.util.http_util import *
from PIL import ImageFile
from loguru import logger

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None










sys.setrecursionlimit(10 ** 5)  # 设置递归最大深度 10的5次方

from src.common.config.config import config

path_folder = config.SPIDER_FOLDER_PATH
import gc


def get_path_folder(pubmed_entity):
    """
    统一规整下载文件路径
    @param pubmed_entity:
    @return:
    """
    return path_folder + pubmed_entity.paper_id + '/'


class ArticleAnalysisService:
    def __init__(self, article=None):
        self.model = lp.Detectron2LayoutModel("./config.yaml",
                                              "./model_final.pth",
                                              extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                              label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"})
        # self.model = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
        #                                       extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
        #                                       label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"})
        self.ocr_agent = lp.TesseractAgent()
        if article is None:
            self.article = Article()
        else:
            self.article = article
        self.image_folder_path = ''

        self.article_entity_dao = ArticleEntityDao()

    def search_analysis_article(self):
        """
        搜索解析文章
        @return:
        """

        article_entity = self.article_entity_dao.query_article_by_state(ARTICLE_STATE.ARTICLE_ANALYSIS_READY.value)

        if article_entity is None:
            return



        try:



            status = self.article_entity_dao.update_article({'state': ARTICLE_STATE.ARTICLE_ANALYSIS_BEGIN.value,
                                           'version': article_entity.version + 1},
                                          [ArticleEntity.id == article_entity.id,
                                           ArticleEntity.version == article_entity.version])
            if status == 0:
                return

            logger.info('解析阶段开始' + article_entity.pmc_id)
            # 开始时间
            start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"解析{article_entity.pmc_id}文章开始时间：{start_time}")

            # Json不存在替换
            if article_entity.article_json is None or len(article_entity.article_json) == 0:
                self.article = Article()
                pubmed_entity = PubmedEntity(title=article_entity.title, pmc_id=article_entity.pmc_id)
                self.article.pubmed_entity = pubmed_entity
            else:
                self.article = parse_json_str_to_article_node(article_entity.article_json)

            self.article.article_entity = article_entity
            self.parse_pdf_file_to_article()
            self.article_entity_dao.update_article(
                {'state': ARTICLE_STATE.ARTICLE_ANNOTATE_READY.value,
                 'article_json': parseArticleToJsonStr(self.article)},
                [ArticleEntity.id == article_entity.id])
            logger.info('解析阶段结束' + article_entity.pmc_id)
            # 结束时间
            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"解析文章结束时间：{end_time}")
            # 所耗用时间
            logger.info('解析' + article_entity.pmc_id + '耗时:' + str(
                datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')))
        except Exception as e:
            import traceback
            exception_str = traceback.format_exc()
            logger.exception('解析阶段失败' + article_entity.pmc_id + exception_str)

            self.article_entity_dao.update_article(
                {'state': ARTICLE_STATE.ARTICLE_ANALYSIS_ERROR.value,
                 'info': exception_str},
                [ArticleEntity.id == article_entity.id])

    def start(self):
        count = 7
        while True:
            if count > 6:
                logger.info('文章解析搜索中')
                count = 0
            else:
                count += 1
            try:
                self.search_analysis_article()
            except Exception as e:
                logger.exception(e)
            time.sleep(10)

    def cmp_layout(self, layout1, layout2):
        """
        布局排序比较
        @param layout1:
        @param layout2:
        @return:
        """
        block1 = layout1.block
        block2 = layout2.block
        # y2轴相同 就按x轴来

        w1 = block1.x_2 - block1.x_1
        w2 = block2.x_2 - block2.x_1
        # 说明是两种类型 按y排列
        if abs(w2 - w1) > 1000:
            return block1.y_2 - block2.y_2

        if self.check_abs(block1.y_2, block2.y_2):
            return block1.x_1 - block2.x_1
        # y2轴不同 先看x轴是否相同  不同优先左边那列
        if self.check_abs(block1.x_1, block2.x_1):
            return block1.y_2 - block2.y_2
        return block1.x_1 - block2.x_1

    # def sortLayout(self, layoutList):
    #     for i in range(len(layoutList)):
    #         for j in range(1, len(layoutList)):
    #             block1 = layoutList[i].block
    #             block2 = layoutList[j].block
    #             w1 = block1.x_2 - block1.x_1
    #             w2 = block2.x_2 - block2.x_1
    #             # 说明是两种类型 按y排列
    #             if abs(w2 - w1) > 1000:
    #                 # 从小到大排列
    #                 if block2.y_2 < block1.y_2:
    #                     temp = layoutList[i]
    #                     layoutList[i] = layoutList[j]
    #                     layoutList[j] = temp
    #                     continue
    #             if self.checkAbs(block1.y_2, block2.y_2):
    #                 if block2.x_1 < block1.x_1:
    #                     temp = layoutList[i]
    #                     layoutList[i] = layoutList[j]
    #                     layoutList[j] = temp
    #                     continue
    #             if self.checkAbs(block1.x_1, block2.x_1):
    #                 if block2.y_2 < block1.y_2:
    #                     temp = layoutList[i]
    #                     layoutList[i] = layoutList[j]
    #                     layoutList[j] = temp
    #                     continue
    #             if block2.x_1 < block1.x_1:
    #                 temp = layoutList[i]
    #                 layoutList[i] = layoutList[j]
    #                 layoutList[j] = temp

    def check_abs(self, a, b):
        """
        检查两个位置的间距
        @param a:
        @param b:
        @return:
        """
        # 如果小于10 可以暂时认为是一个位置？
        if abs(a - b) < 200:
            return True
        return False

    def parse_pdf_file_to_article(self):

        """
        将pdf转换为文章结构
        """
        # 检测本地有没有该pdf 如果没有则需要重新下载
        pdf_path = self.article.pubmed_entity.download_path

        if os.path.exists(pdf_path):
            logger.info("文件存在")
        else:
            logger.info("文件不存在")
            pubmed_entity = self.article.pubmed_entity
            is_success, pdf_path = get_file_from_url(get_path_folder(pubmed_entity),
                                                     pubmed_entity.paper_id + '_' + pubmed_entity.title,
                                                     self.article.article_entity.pdf_oss_url)
            if is_success is not True:
                logger.info('下载失败')
                self.article.article_entity.state = ARTICLE_STATE.ARTICLE_ANALYSIS_ERROR.value
                self.article.article_entity.info = 'PDF 获取失败'
                return
            else:
                logger.info('下载成功')

        # 获取文件夹存储路径 底下添加图片路径
        image_folder_path = get_path_folder(self.article.pubmed_entity) + 'images/'

        logger.info('开始pdf转为图片' + self.article.article_entity.pmc_id)
        self.image_folder_path = image_folder_path
        image_path_list = convert_pdf_to_image(pdf_path, image_folder_path)
        logger.info('pdf转为图片结束' + self.article.article_entity.pmc_id)
        logger.info('开始图片布局解析' + self.article.article_entity.pmc_id)
        self.parse_image_list_new(image_path_list)
        logger.info('图片布局解析结束' + self.article.article_entity.pmc_id)
        logger.info('开始删除图片' + self.article.article_entity.pmc_id)
        del_file(image_folder_path)
        logger.info('图片删除结束' + self.article.article_entity.pmc_id)

        return self.article

    def parse_image_list(self, image_path_list):
        """
        转换图片list
        @param image_path_list:
        """
        layout_list = []
        image_list = []
        logger.info('开始获取图片布局' + self.article.article_entity.pmc_id)
        memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        logger.info(f"当前进程的内存占用: {memory_usage} KB")

        for i in range(len(image_path_list)):
            logger.info(
                '获取图片布局' + self.article.article_entity.pmc_id + ':' + str(i + 1) + '/' + str(
                    len(image_path_list)))
            temp_layout_list, temp_image_list = self.parse_image_layout(image_path_list[i])
            layout_list.extend(temp_layout_list)
            image_list.extend(temp_image_list)

        memory_usage_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        logger.info(f"执行代码后的内存占用: {memory_usage_after} KB")
        # 计算内存使用增长
        memory_increase = memory_usage_after - memory_usage
        logger.info(f"内存增长: {memory_increase} KB")

        logger.info('获取图片布局结束' + self.article.article_entity.pmc_id)
        memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        logger.info(f"当前进程的内存占用: {memory_usage} KB")
        logger.info('开始解析图片内容' + self.article.article_entity.pmc_id)
        self.build_article(layout_list, image_list)
        logger.info('解析图片内容结束' + self.article.article_entity.pmc_id)
        memory_usage_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        logger.info(f"执行代码后的内存占用: {memory_usage_after} KB")
        # 计算内存使用增长
        memory_increase = memory_usage_after - memory_usage
        logger.info(f"内存增长: {memory_increase} KB")

    def parse_image_list_new(self, image_path_list):
        """
        转换内容 使用迭代的方式 不会一次性转为全部
        @param image_path_list:
        """

        logger.info('开始获取图片布局' + self.article.article_entity.pmc_id)

        # 根节点
        root_node = None
        # 上一个节点
        pre_node_list = []
        pre_type = ParseLayoutType.TITLE
        figure_list = []
        figure_index = 1

        for j in range(len(image_path_list)):

            memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            logger.info(f"当前进程的内存占用: {memory_usage} KB")

            logger.info(
                '获取图片布局' + self.article.article_entity.pmc_id + ':' + str(j + 1) + '/' + str(
                    len(image_path_list)))
            # 返回该图片下的所有解析
            layout_list, image_list = self.parse_image_layout(image_path_list[j])
            # layoutList.extend(tempLayoutList)
            # imageList.extend(tempImageList)

            # 遍历Layout解析内容
            for i in range(len(layout_list)):
                logger.info(
                    '解析图片内容+' + str(j + 1) + self.article.article_entity.pmc_id + ':' + str(i + 1) + '/' + str(
                        len(layout_list)))
                layout = layout_list[i]
                if layout.type == ParseLayoutType.TITLE.value:
                    text = self.ocr_agent.detect(image_list[i])
                    font_size = self.get_font_size(image_list[i].shape[0], image_list[i].shape[1], text)
                    if root_node is None:
                        root_node = ArticleNode(nodeType=ArticleNodeType.ROOT, content=text, fontSize=font_size)
                        pre_node_list.append(root_node)
                    else:
                        temp = len(pre_node_list) - 1
                        while temp > 0:
                            # 说明是一个级别的 list出栈
                            if abs(pre_node_list[temp].fontSize - font_size) < 3:
                                pre_node_list.pop()
                                temp -= 1
                            else:
                                break

                        temp_node = ArticleNode(nodeType=ArticleNodeType.TITLE, content=text, fontSize=font_size)
                        # 父节点
                        if len(pre_node_list) > 0:
                            father_node = pre_node_list[-1]
                            father_node.put(temp_node)
                        pre_node_list.append(temp_node)
                    pre_type = ParseLayoutType.TITLE
                # elif layout.type == ParseLayoutType.TEXT.value:
                elif layout.type == ParseLayoutType.TEXT.value or layout.type == ParseLayoutType.LIST.value:
                    # 获取ocr检测的内容
                    text = self.ocr_agent.detect(image_list[i])

                    if pre_type == ParseLayoutType.FIGURE:
                        if len(figure_list) > 0:
                            figure_list[-1].content = text
                    else:
                        font_size = self.get_font_size(image_list[i].shape[0], image_list[i].shape[1], text)
                        temp_node = ArticleNode(nodeType=ArticleNodeType.PARAGRAPH, content=text, fontSize=font_size)

                        if len(pre_node_list) > 0:
                            father_node = pre_node_list[-1]
                            father_node.put(temp_node)
                    pre_type = ParseLayoutType.TEXT

                elif layout.type == ParseLayoutType.FIGURE.value:
                    path = self.image_folder_path + 'fg' + str(figure_index) + '.png'
                    cv2.imwrite(path, image_list[i])
                    figure = Figure(url=path, index='fg' + str(figure_index))
                    figure_index += 1

                    figure_list.append(figure)
                    pre_type = ParseLayoutType.FIGURE
                else:
                    pre_type = ParseLayoutType.TABLE

            memory_usage_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            logger.info(f"执行代码后的内存占用: {memory_usage_after} KB")
            # 计算内存使用增长
            memory_increase = memory_usage_after - memory_usage
            logger.info(f"内存增长: {memory_increase} KB")
            layout_list.clear()
            image_list.clear()
            logger.info(f"执行GC代码后的内存占用: {memory_usage_after} KB")
            # 计算内存使用增长
            memory_increase = memory_usage_after - memory_usage
            logger.info(f"内存增长: {memory_increase} KB")

        logger.info('获取图片布局结束' + self.article.article_entity.pmc_id)

        # startGpu()
        # memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # print(f"当前进程的内存占用: {memory_usage} KB")
        # print('开始解析图片内容' + self.article.articleEntity.pmc_id)
        # self.buildArticle(layoutList, imageList)
        # print('解析图片内容结束' + self.article.articleEntity.pmc_id)
        # memory_usage_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # print(f"执行代码后的内存占用: {memory_usage_after} KB")
        # endGpu()
        # 计算内存使用增长
        # memory_increase = memory_usage_after - memory_usage
        # print(f"内存增长: {memory_increase} KB")

        gc.collect()
        root_node.index = '0'
        self.set_node_index(root_node, '')
        self.article.article_node = root_node
        self.article.figures = self.process_images(figure_list)

    def process_images(self, figure_list):
        """
        处理图片信息
        @param figure_list:
        @return:
        """
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d')
        download_path = self.article.pubmed_entity.download_path
        paper_id = self.article.pubmed_entity.paper_id
        for i in range(len(figure_list)):
            path = figure_list[i].url
            # 获取前面的path
            com_path = path.rstrip('.png') + '-com.png'

            im = Image.open(path)
            logger.info(com_path)
            im.save(com_path, quality=1)
            url = upload_file(com_path,
                              'pdf/' + timestamp + '/' + paper_id + '/images/' + paper_id + str(i + 1) + 'png')
            figure_list[i].url = url
        #     newFigureList.append(url)

        # 删除原有图片
        return figure_list

    def build_article(self, layout_list, image_list):
        """
        构建文章
        @param layout_list:
        @param image_list:
        """
        # 根节点
        root_node = None
        # 上一个节点
        pre_node_list = []
        pre_type = ParseLayoutType.TITLE
        figure_list = []
        figureIndex = 1
        # 遍历Layout解析内容
        for i in range(len(layout_list)):
            logger.info('解析图片内容' + self.article.article_entity.pmc_id + ':' + str(i + 1) + '/' + str(len(layout_list)))
            layout = layout_list[i]
            if layout.type == ParseLayoutType.TITLE.value:
                text = self.ocr_agent.detect(image_list[i])
                font_size = self.get_font_size(image_list[i].shape[0], image_list[i].shape[1], text)
                if root_node is None:
                    root_node = ArticleNode(nodeType=ArticleNodeType.ROOT, content=text, fontSize=font_size)
                    pre_node_list.append(root_node)
                else:
                    temp = len(pre_node_list) - 1
                    while temp > 0:
                        # 说明是一个级别的 list出栈
                        if abs(pre_node_list[temp].fontSize - font_size) < 3:
                            pre_node_list.pop()
                            temp -= 1
                        else:
                            break
                    # 父节点
                    father_node = pre_node_list[-1]
                    temp_node = ArticleNode(nodeType=ArticleNodeType.TITLE, content=text, fontSize=font_size)
                    father_node.put(temp_node)
                    pre_node_list.append(temp_node)
                pre_type = ParseLayoutType.TITLE
            # elif layout.type == ParseLayoutType.TEXT.value:
            elif layout.type == ParseLayoutType.TEXT.value or layout.type == ParseLayoutType.LIST.value:

                text = self.ocr_agent.detect(image_list[i])

                if pre_type == ParseLayoutType.FIGURE:
                    figure_list[-1].content = text
                else:
                    father_node = pre_node_list[-1]
                    font_size = self.get_font_size(image_list[i].shape[0], image_list[i].shape[1], text)
                    temp_node = ArticleNode(nodeType=ArticleNodeType.PARAGRAPH, content=text, fontSize=font_size)
                    father_node.put(temp_node)
                pre_type = ParseLayoutType.TEXT

            elif layout.type == ParseLayoutType.FIGURE.value:
                path = self.image_folder_path + 'fg' + str(figureIndex) + '.png'
                cv2.imwrite(path, image_list[i])
                figure = Figure(url=path, index='fg' + str(figureIndex))
                figureIndex += 1

                figure_list.append(figure)
                pre_type = ParseLayoutType.FIGURE
            else:
                pre_type = ParseLayoutType.TABLE

        root_node.index = '0'
        self.set_node_index(root_node, '')
        self.article.article_node = root_node
        self.article.figures = figure_list

    def set_node_index(self, article_node, index):
        """
        设置节点索引
        @param article_node:
        @param index:
        @return:
        """
        if article_node.nodeType != ArticleNodeType.ROOT:
            article_node.index = index
            index += '.'

        if article_node.nodeType == ArticleNodeType.PARAGRAPH:
            self.parse_node_to_sentence(article_node)
            return

        if len(article_node.nodes) > 0:
            i = 1
            for node in article_node.nodes:
                self.set_node_index(node, index + str(i))
                i += 1

    def parse_node_to_sentence(self, article_node):
        """
        将节点转为句子
        @param article_node:
        """
        content = article_node.content
        text_list = content.split("\n")
        new_content = ''
        for text in text_list:
            if len(text.strip()) < 1:
                continue
            # TODO 考虑如何合并假回车以及段落
            new_content += (text.strip())
        sentences = split_sentences(new_content)
        index = article_node.index
        nodes = []
        i = 1
        for sentence in sentences:
            temp_node = ArticleNode(index=index + '.' + str(i), nodeType=ArticleNodeType.SENTENCE, content=sentence,
                                    fontSize=article_node.fontSize)
            nodes.append(temp_node)
            i += 1
        article_node.nodes = nodes

    def parse_image_layout(self, path):
        image = cv2.imread(path)
        image = image[..., ::-1]
        image_list = []
        layout = self.model.detect(image)
        # TODO 临时做法
        pre_path = path.rstrip('.png')
        i = 0
        # print(pre_path)
        if not os.path.exists(pre_path):
            os.mkdir(pre_path)
        pre_path += '\\'

        # text_blocks = lp.Layout([b for b in layout if b.type == 'Text'])  # 循环浏览页面上的每个文本框。
        # for block in text_blocks:
        #     print(block)
        #     print(block.block.x_1)
        #     segment_image = (block
        #                      .pad(left=5, right=5, top=5, bottom=5)
        #                      .crop_image(image))
        #     # add padding in each image segment can help
        #     # improve robustness
        #
        #     text = self.ocr_agent.detect(segment_image)
        #     print(text)
        #     self.getFontSize(segment_image.shape[0], segment_image.shape[1], len(text))
        #     cv2.imwrite(pre_path + 'text' + str(i) + '.png', segment_image)
        #     i += 1
        # i = 0
        # figure_blocks = lp.Layout([b for b in layout if b.type == 'Figure'])
        # # 循环浏览页面上的每个文本框。
        # for block in figure_blocks:
        #     segment_image = (block
        #                      .pad(left=5, right=5, top=5, bottom=5)
        #                      .crop_image(image))
        #     # text = self.ocr_agent.detect(segment_image)
        #     # self.getFontSize(segment_image.shape[0],segment_image.shape[1],len(text))
        #     cv2.imwrite(pre_path + 'figure' + str(i) + '.png', segment_image)
        #     i += 1
        #
        # i = 0
        # title_blocks = lp.Layout([b for b in layout if b.type == 'Title'])  # 循环浏览页面上的每个文本框。
        # for block in title_blocks:
        #     segment_image = (block
        #                      .pad(left=5, right=5, top=5, bottom=5)
        #                      .crop_image(image))
        #     text = self.ocr_agent.detect(segment_image)
        #     self.getFontSize(segment_image.shape[0], segment_image.shape[1], len(text))
        #     print(text)
        #
        #     cv2.imwrite(pre_path + 'title' + str(i) + '.png', segment_image)
        #     i += 1
        #
        # i = 0
        # table_blocks = lp.Layout([b for b in layout if b.type == 'Table'])  # 循环浏览页面上的每个文本框。
        # for block in table_blocks:
        #     segment_image = (block
        #                      .pad(left=5, right=5, top=5, bottom=5)
        #                      .crop_image(image))
        #     # text = self.ocr_agent.detect(segment_image)
        #     # self.getFontSize(segment_image.shape[0],segment_image.shape[1],len(text))
        #     cv2.imwrite(pre_path + 'table' + str(i) + '.png', segment_image)
        #     i += 1

        # 展示输出的PNG
        show_image = lp.draw_box(image, layout, box_width=3, show_element_type=True)
        show_image.save(pre_path + 'layout.png')

        result = sorted(layout, key=cmp_to_key(self.cmp_layout))
        # i = 0
        # for block in result:
        #     # print(block)
        #     # print(block.block.x_1)
        # TODO 这个可以考虑看情况进行添加 多扩张一点
        #     # block.block.y_1 -= 200
        #     segment_image = (block
        #                      .pad(left=5, right=5, top=5, bottom=5)
        #                      .crop_image(image))
        #     # add padding in each image segment can help
        #     # improve robustness
        #
        #     text = self.ocr_agent.detect(segment_image)
        #     print(text)
        #     cv2.imwrite(pre_path + 'text' + str(i) + '.png', segment_image)
        #     i += 1

        # self.sortLayout(layout)
        # text_blocks = [b for b in result if b.type == 'Text']  # 循环浏览页面上的每个文本框。
        # for block in text_blocks:
        #     print(block)
        #     print(block.block.x_1)
        #     segment_image = (block
        #                      .pad(left=5, right=5, top=5, bottom=5)
        #                      .crop_image(image))
        #     # add padding in each image segment can help
        #     # improve robustness
        #
        #     text = self.ocr_agent.detect(segment_image)
        #     print(text)
        #     self.getFontSize(segment_image.shape[0], segment_image.shape[1], len(text))

        #     i += 1

        for block in result:
            segment_image = (block
                             .pad(left=5, right=5, top=5, bottom=5)
                             .crop_image(image))
            image_list.append(segment_image)

        return result, image_list

    def get_font_size(self, width, height, text):
        """
        获取字体大小
        @param width:
        @param height:
        @param text:
        @return:
        """
        text_list = text.split("\n")
        new_text_list = []
        for text in text_list:
            if len(text.strip()) < 1:
                continue
            new_text_list.append(text.strip())
        text_len = len(new_text_list)
        if text_len == 0:
            return 0
        if text_len < 3:
            font_size = width * height / 1000 / len(text_list[0]) / text_len
            return font_size
        length = 0
        for i in range(1, text_len - 1):
            length += len(new_text_list[i])
        font_size = width * (text_len - 2) * height / text_len / 1000 / length
        return font_size
