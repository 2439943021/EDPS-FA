package com.analysis.service;

import com.qiniu.util.Auth;
import com.qiniu.util.StringMap;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Transactional
@Slf4j
@Service
public class QiNiuYunOssService {
    @Value("${qiniu.accessKey}")
    String accessKey;
    @Value("${qiniu.secretKey}")
    String secretKey;
    @Value("${qiniu.bucket}")
    String bucket;

    /**
     * 生成七牛云上传token
     */
    public String policy() {
        Auth auth = Auth.create(accessKey, secretKey);
        StringMap policy = new StringMap();
        // 设置上传策略的过期时间为当前时间的60秒钟后
        log.info("当前时间为：{}", System.currentTimeMillis() / 1000L);
        String upToken = auth.uploadToken(bucket, null, 60, policy);
        return upToken;
    }
}
