package com.analysis.api;

/**
 * @author ChenJG
 * @date 2024/6/12 20:34
 */
public interface IResultCode {
    long getCode();

    /**
     * 返回信息
     */
    String getMessage();
}
