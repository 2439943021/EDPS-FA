package com.analysis.dto.articledto;

import io.swagger.annotations.ApiModel;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.List;

@Data
@Accessors(chain = true)
@ApiModel("文章JSON")
public class ArticleJsonDto {
    List<FiguresDto> figures;
    String articleNode;
    PubmedEntityDto pubmed_entity;
}
