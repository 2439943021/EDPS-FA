package com.analysis.controller;

import com.analysis.api.CommonResult;
import com.analysis.service.QiNiuYunOssService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OssController {
    @Autowired
    QiNiuYunOssService qiNiuYunOssService;

    @GetMapping("/oss/policy")
    public CommonResult<String> policy() {
        String upToken = qiNiuYunOssService.policy();
        return CommonResult.success(upToken);
    }
}
