package com.analysis.entity;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableLogic;
import com.baomidou.mybatisplus.annotation.TableName;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

import java.util.Date;

/**
 * @author ChenJG
 * @date 2024/3/12 0:05
 */
@Data
@TableName("article")
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = false)
@ApiModel("文章")
public class Article {
    @TableId(type = IdType.ASSIGN_ID)
    public String id;
    @ApiModelProperty("可见状态")
    @TableLogic(value = "01",delval = "00")
    public  String visible;
    @ApiModelProperty("文章id")
    private String pmcId;
    @ApiModelProperty("检测状态")
    private String state;
    @ApiModelProperty("文章json")
    private String articleJson;
    @ApiModelProperty("文章类型")
    private Integer articleType;
    @ApiModelProperty("pdf_pubmed_url")
    private String pdfPubmedUrl;
    @ApiModelProperty("pdf_spider_url")
    private String pdfSpiderUrl;
    @ApiModelProperty("pdf_oss_url")
    private String pdfOssUrl;
    @ApiModelProperty("pdf_path")
    private String pdfPath;
    @ApiModelProperty("html_path")
    private String htmlPath;
    @ApiModelProperty("html_url")
    private String htmlUrl;
    @ApiModelProperty("文章标题")
    private String title;
    @ApiModelProperty("第一作者")
    private String author;
    @ApiModelProperty("用户id")
    private Long userId;
    @ApiModelProperty("额外信息")
    private String info;
    @ApiModelProperty("版本号")
    private Integer version;
    @ApiModelProperty("创建文章检测时间")
    private Date createTime;
    @ApiModelProperty("开始时间")
    private Date startTime;
    @ApiModelProperty("结束时间")
    private Date endTime;
    @ApiModelProperty("更新时间")
    private Date updateTime;
    @ApiModelProperty("提交类型")
    private String submitType;
    @ApiModelProperty("pdf完成状态")
    private String pdfCompletion;
    @ApiModelProperty("大模板ID")
    private String templateBigId;
    @ApiModelProperty("大模板名称")
    private String templateBigName;
    @ApiModelProperty("excel报告oss地址")
    private String excelUrl;
    @ApiModelProperty("excel报告本地路径")
    private String excelPath;
    @ApiModelProperty("报告打包本地路径")
    private String zipPath;
    @ApiModelProperty("报告打包oss地址")
    private String zipUrl;
}
