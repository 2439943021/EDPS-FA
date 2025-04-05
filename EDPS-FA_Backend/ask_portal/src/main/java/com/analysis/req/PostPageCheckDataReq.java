package com.analysis.req;

import io.swagger.annotations.ApiModel;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@ApiModel("用于根据pmcId、state对报告进行模糊查询和查询所有报告")
public class PostPageCheckDataReq {
    String pmcId;
    String state;
    String title;
}
