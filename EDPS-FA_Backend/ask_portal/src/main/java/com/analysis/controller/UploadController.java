package com.analysis.controller;

import com.analysis.service.ArticleService;
import com.analysis.dto.articledto.UploadReceiveByPmcIdsDto;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@Log4j2
@RestController
@RequestMapping("/upload")
public class UploadController {

    @Autowired
    private ArticleService articleService;

    @PostMapping("/uploadbyPDF")
    public String insertPostByPDF(@RequestBody UploadReceiveByPmcIdsDto uploadReceiveByPmcIdsDto) {
        boolean result = articleService.insertPostByExcel(uploadReceiveByPmcIdsDto);
        if(result){
            return "true";
        }
        else return "false";
    }
}
