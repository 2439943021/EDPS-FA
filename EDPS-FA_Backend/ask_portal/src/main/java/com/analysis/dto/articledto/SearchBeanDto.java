package com.analysis.dto.articledto;

import io.swagger.annotations.ApiModel;
import lombok.Data;

@Data
@ApiModel("前端传来数据的类型")
public class SearchBeanDto<T> {
    private Integer pageNum;
    private Integer pageSize;
    private T data;
}
