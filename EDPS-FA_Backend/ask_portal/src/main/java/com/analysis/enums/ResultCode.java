package com.analysis.enums;

import com.analysis.api.IResultCode;
import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 返回结果代码
 * @author ChenJG
 * @date 2024/6/12 20:34
 */
@AllArgsConstructor
@Getter
public enum ResultCode implements IResultCode {
    SUCCESS(0, "操作成功"),
    FAILED(500, "操作失败"),
    VALIDATE_FAILED(400, "参数检验失败"),
    UNAUTHORIZED(401, "认证失败"),
    FORBIDDEN(403, "没有相关权限");
    private long code;
    private String message;
}


