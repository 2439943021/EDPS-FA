package com.analysis.controller;


import com.analysis.api.CommonResult;
import com.analysis.dto.articledto.SearchBeanDto;
import com.analysis.entity.Article;
import com.analysis.req.PostPageCheckDataReq;
import com.analysis.service.ArticleService;
import com.baomidou.mybatisplus.core.metadata.IPage;
import io.swagger.annotations.Api;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * @author LiGan
 * @date 2024/3/14 17:26
 * @description
 */
@RequestMapping("/check/")
@RestController
@Api("查看报告")
public class CheckArticleController {
    @Autowired
    private ArticleService articleService;

    @PostMapping("/checkArticleInfo")
    public CommonResult<IPage<Article>> checkArcticleInfo(@RequestBody SearchBeanDto<PostPageCheckDataReq> searchBeanDto){
        IPage<Article> page = articleService.checkArticleInfo(searchBeanDto);
        return CommonResult.success(page);
    }

    @GetMapping("/checkArticleJson")
    public String checkArticleJson(@RequestParam String id){
        String result = articleService.checkArticleJson(id);
        return result;
    }
}
