package com.analysis.dto.articledto;

import io.swagger.annotations.ApiModel;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.List;

@Data
@Accessors(chain = true)
@ApiModel("文章实体")
public class UploadReceiveByPmcIdsDto {
    List<String> infos;
}
