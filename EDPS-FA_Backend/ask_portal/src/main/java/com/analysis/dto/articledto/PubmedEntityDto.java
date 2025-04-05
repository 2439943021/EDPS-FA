package com.analysis.dto.articledto;

import io.swagger.annotations.ApiModel;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@ApiModel("PubmedEntityDto")
public class PubmedEntityDto {
    String pmc_id;
    String title;
    String author_list;
}
