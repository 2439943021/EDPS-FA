package com.analysis.dto.articledto;

import io.swagger.annotations.ApiModel;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@ApiModel("FiguresDto")
public class FiguresDto {
    String content;
    String url;
    String index;
}
