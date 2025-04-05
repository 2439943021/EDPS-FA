package com.analysis.mapper;

import com.analysis.entity.Article;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.mapstruct.Mapper;

import java.util.List;

/**
 * @author ChenJG
 * @date 2024/3/12 0:11
 */
@Mapper
public interface ArticleMapper extends BaseMapper<Article> {

//    List<ArticlePojo> findAllResult(Integer maxRecord, Integer index);
//    List<ArticlePojo> findAllResultByPmcId(String pmcId,Integer maxRecord, Integer index);
//    ArticlePojo findUrl(String id);
//    ArticlePojo selectByPmcId(String pmcId);
//    Integer insertByPmcId(String pmcId);
//    Integer insertByPmcIdToArticle(String Id,String pmcId);
//    Integer findAllCount();
//    Integer findAllCountByState(String stateCode);
//    Integer findAllCountByPmcId(String pmcId);
//
//    List<ArticlePojo> checkByState(String stateCode,Integer maxRecord, Integer index);
    List<Article> selectByPmcId(String pmcId);
}
