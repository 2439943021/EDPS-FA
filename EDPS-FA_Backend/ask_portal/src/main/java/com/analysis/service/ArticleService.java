package com.analysis.service;

import cn.hutool.json.JSONUtil;
import com.alibaba.fastjson.JSON;
import com.analysis.dto.articledto.*;
import com.analysis.entity.Article;
import com.analysis.mapper.ArticleMapper;
import com.analysis.req.PostPageCheckDataReq;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

@Log4j2
@Transactional
@Service
public class ArticleService extends ServiceImpl<ArticleMapper, Article> {
    /**
     * 根据PDF上传报告
     *
     * @param uploadReceiveByPmcIdsDto
     * @return boolean
     */
    @Autowired
    private ArticleMapper articleMapper;
    public boolean insertPostByExcel(UploadReceiveByPmcIdsDto uploadReceiveByPmcIdsDto) {
        List<String> infos = uploadReceiveByPmcIdsDto.getInfos();
        Integer length = 0;
        Iterator<String> iterator1 = infos.iterator();

        while (iterator1.hasNext()) {
            length++;
            String info = iterator1.next();
            String pmcId = info.split("#")[0];
            String url = info.split("#")[1];
            if (length <= 1000) {        //设置最大限制长度
                //创建一个Article实体类，将添加的信息放入其中
                Article article = new Article();
                article.setPmcId(pmcId);
                article.setState("21");
                article.setSubmitType("03");
                article.setPdfOssUrl(url);
                //将数据插入到数据库中的对应表中
                save(article);
            }
        }
        return true;
    }

    /**
     * 查看文章
     *
     * @param searchBeanDto
     * @return IPage
     */
    public IPage<Article> checkArticleInfo(SearchBeanDto<PostPageCheckDataReq> searchBeanDto) {

        IPage<Article> page = new Page<>(searchBeanDto.getPageNum(), searchBeanDto.getPageSize());
        LambdaQueryWrapper<Article> queryWrapper = new LambdaQueryWrapper<>();

        PostPageCheckDataReq reqData = searchBeanDto.getData();
        if (StringUtils.hasLength(reqData.getPmcId())) {
            queryWrapper.like(Article::getPmcId, reqData.getPmcId());
        }
        if (StringUtils.hasLength(reqData.getState())) {
            queryWrapper.like(Article::getState, reqData.getState());
        }
        if (StringUtils.hasLength(reqData.getTitle())) {
            queryWrapper.like(Article::getTitle, reqData.getTitle());
        }

        queryWrapper.orderByDesc(Article::getCreateTime);

        this.page(page, queryWrapper);

        // 修改title和authr字段
        List<Article> articles = page.getRecords();
        for (Article article : articles) {
            ArticleJsonDto articleJsonDto = JSON.parseObject(article.getArticleJson(),ArticleJsonDto.class);
            PubmedEntityDto pubmedEntityDto = articleJsonDto.getPubmed_entity();
            if(article.getTitle() == null){
                article.setTitle(pubmedEntityDto.getTitle());
                articleMapper.updateById(article);
            }
            article.setTitle(pubmedEntityDto.getTitle());
            article.setAuthor(null);
            article.setArticleJson(null);
        }
        return page;
    }
    /**
     * 文章JSON信息提取
     *
     * @param id
     * @return boolean
     */
    public String checkArticleJson(String id) {
        LambdaQueryWrapper<Article> queryWrapper = new LambdaQueryWrapper<>();
        queryWrapper.eq(Article::getId, id);
        System.out.println(id);
        Article article = articleMapper.selectById(id);
        ArticleJsonDto articleJsonDto = JSON.parseObject(article.getArticleJson(),ArticleJsonDto.class);

        System.out.println("_______________________________________");
        System.out.println(JSONUtil.toJsonStr(articleJsonDto.getFigures()));

        List<FiguresDto> figuresDtoList = articleJsonDto.getFigures();
        //遍历文章的图表信息
        //存放图表的说明内容
        List<String> content = new ArrayList<>();
        //存放图标的url地址
        List<String> url = new ArrayList<>();
        for(FiguresDto figuresDto:figuresDtoList){
            content.add(figuresDto.getContent());
            url.add(figuresDto.getUrl());
        }
        System.out.println(content);
        System.out.println(url);




        System.out.println("_______________________________________");
        System.out.println(JSONUtil.toJsonStr(articleJsonDto.getArticleNode()));





        System.out.println("_______________________________________");
        System.out.println(JSONUtil.toJsonStr(articleJsonDto.getPubmed_entity()));
        System.out.println("_______________________________________");

        return "true";
    }
}
