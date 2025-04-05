import { get } from '../utils/index'
import { post } from '../utils/index'
import { Delete } from '../utils/index'

/**
 * 微信登录接口
 */
// 获取微信登录二维码
export function getQrCode(){
    return get('/weixin/generate',{});
}
// 轮询接口
export function isScanQrcode(code:string){
    return get('/weixin/check', {code});
}

export function login(){
    return get('/wx/login', {});
}
/**
 * 
 * 提交检测接口
 */
// 根据pmcid获取文章htmlUrl
export function getPostByPmcid(pmcId: any){
    return get('/check/checkPost', {pmcId});
}

// 根据用户id获取所有大模板
export function checkAllTemplateByUserId(userId:number){
    return get(`/template/checkAllBigTemplateByUserIdList/${userId}`, {});
}

// 以excle文件获得多个pmid 
export function PostByExcle(data: any, bigTempId:string, bigTempName:string,userId:number){
    return post('/upload/uploadbyExcel', {pmcIds:data, submitType:"02",
    userId:userId, templateBigId:bigTempId, templateBigName:bigTempName});
}

// 提交检测pmid 
export function PostByPmids(data: any, bigTempId:string, bigTempName:string, userId:number){
    return post('/upload/uploadbypmcid', {pmcIds:data, submitType:"01",
    userId:userId, templateBigId:bigTempId, templateBigName:bigTempName});
}

// 以pdf或压缩文件提交检测
export function PostByPdfs(formData:FormData){
    return post('http://119.8.32.97:8055/api/upload/uploadbyPdf', formData,{
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
}
// 上传七牛云获取token 
export function getTokenByQiniu(){
    return get('/oss/policy', {});
}

// 将对应的pdf写入数据库
export function insertPdfToDataBase(userId:number, templateBigId:string,templateBigName:string,
    title:string, url:string, pmcId:string){
    return post('/oss/insertPostByPdf', {userId, templateBigId, templateBigName, submitType:'03',
    title, url, pmcId})
}

/**
 * 
 * 查看报告接口
 */

// 获取文章列表
export function getList(maxRecord:any, index: any, userId:number){
    return post('/check/checkPostInfo', {pageSize:maxRecord,pageNum:index, data:{pmcId:'', state:'', userId}});
}

// 根据文章状态和pimcd模糊搜索
export function postCheckByStateAndPmcId(pmcId:any, maxRecord:any, index:any, state:any, userId:number){
    return post('/check/checkPostInfo', {pageSize:maxRecord, pageNum:index, data:{pmcId, state, userId}})
}

// 根据id删除指定报告
export function deleteByPimd(id:string){
    return Delete(`/check/deleteById/${id}`);
}

/**
 * 
 * 自定义模板接口
 */

// 获取所有大模板数据在List页面展示
export function checkAllTemplate(pageNum:number, pageSize:number,userId:number){
    return post('/template/checkAllBigTemplateByUserId', {pageNum, pageSize, data:{userId}})
}

// 获取所有大模板中小模版数据在edit页面展示
export function getSmallInfo(id:any){
    return get(`/template/checkBigTemplateInfo/${id}`, {});
}

// 根据小模版id、pageNum、pageSize获取分页
export function getMoreSmallById(smallId:any, pageNum:any, pageSize:any){
    return post('/template/checkSmallTemplateByPage', {smallId,pageNum,pageSize})
}
// 根据大模板id拷贝
export function copyByBigTempId(id:any, userId:any){
    return post('/template/copyBigTemplate', {id, userId})
}

// 根据大模板id删除大模板
// export function deleteByUserId(id:any, userId:number){
//     return Delete(`/template/deleteByTemplateBigId/?id=${id}&userId=${userId}`);
// }

export function deleteByUserId(tempId:string, userId:number){
    return Delete('/template/deleteByTemplateBigId', {
        "id":tempId, 
        "userId":userId
    });
}
/** 
 * 点击编辑后的相关接口 
 */ 
// 根据大模板id、小模版id删除一对(关键词:相关信息)
export function deleteByBigtempidAndSmallid(oldKey:string,oldValue:string, bigTempId:string, smallTempId:string){
    return Delete('/template/deleteKeyValue', {
        "oldKey":oldKey,
        "newKey":"",
        "oldValue":oldValue,
        "newValue":"",
        "color":"",
        "valid": "",
        "typeName":"",
        "bigTemplateId":bigTempId,
        "smallTemplateId":smallTempId
    })
}

// 根据大模板id、小模版id增加一对(关键词:相关信息)
export function addByBigtempidAndSmallid(newdKey:string,newValue:string, bigTempId:string, smallTempId:string){
    return post('/template/addKeyValue', {
        "oldKey":"",
        "newKey":newdKey,
        "oldValue":"",
        "newValue":newValue,
        "color":"",
        "valid": "",
        "typeName":"",
        "bigTemplateId":bigTempId,
        "smallTemplateId":smallTempId
    })
}

// 根据大模板id、小模版id修改一对(关键词:相关信息)
export function modifyByBigtempidAndSmallid(oldKey:string,oldValue:string, newKey:string, newValue:string,bigTempId:string, smallTempId:string){
    return post('/template/deleteKeyValue', {
        "oldKey":oldKey,
        "newKey":newKey,
        "oldValue":oldValue,
        "newValue":newValue,
        "color":"",
        "valid": "",
        "typeName":"",
        "bigTemplateId":bigTempId,
        "smallTemplateId":smallTempId
    })
}

// 根据大模板id、小模版id更新小模版名称
export function updateByBigtempidAndSmallid(smallName:string, bigTempId:string, smallTempId:string){
    return post('/template/updateSmallTemplateTypeName', {
        "oldKey":"",
        "newKey":"",
        "oldValue":"",
        "newValue":"",
        "color":"",
        "valid": "",
        "typeName":smallName,
        "bigTemplateId":bigTempId,
        "smallTemplateId":smallTempId
    });
}

// 在编辑编辑页面根据大模板id更新大模板信息
export function updateByBigtempId(bigTempId:string,bigTempName:string,bigTempType:string,bigTempDescription:string,){
    return post('/template/updateBigTemplateTopInfo', {
        "id":bigTempId,
        "templateType":bigTempType,
        "templateDescription":bigTempDescription,
        "templateName":bigTempName,
        "small_temp_id":"",
        "volid":"",
        "color":""
    });
}

// 根据大模板id、小模版id，开关值变化判断是否启用小模版
export function enableSmallTemp(bigTempId:string,smallTempId:string,valid:string){
    return post('/template/updateBigTemplateValid', {
        "id":bigTempId,
        "templateName":"",
        "templateType":"",
        "templateDescription":"",
        "small_temp_id":smallTempId,
        "valid":valid,
        "color":""
    });
}

// 根据大模板id、小模版id，颜色值变化判断是否改变小模版所标记的颜色
export function enableColor(bigTempId:string,smallTempId:string,color:string){
    return post('/template/updateBigTemplateColor', {
        "id":bigTempId,
        "templateName":"",
        "templateType":"",
        "templateDescription":"",
        "small_temp_id":smallTempId,
        "valid":"",
        "color":color
    });
}

// 在编辑中增加小模版
export function addSmallTemp(data:string){
    return post('/template/addSmallTemplate', {data:data}); 
}

// 在编辑中删除小模版
export function deleteSmallTemp(templateBigId:string, templateSmallId:string){
    return Delete('/template/deleteSmallTemplate', {templateBigId, templateSmallId}); 
}

// 新建自定模板
export function createTempToJson(data:string){
    return post('/template/addBigTemplate', {data:data});
}

//文件导入小模版
export function importFileSmallTemp(formData:FormData){
    return post('/upload/addSmallTemplateByExcel', formData,{
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
}

// 文件导入大模板
export function importFileBigTemp(formData:FormData){
    return post('/upload/addBigTemplateByExcel', formData,{
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
}
/** 
 * 
 * 检验会员上传
*/

export function checkVipInfo(userId:number){
    return get(`user/userCheckVipInfo/${userId}`, {});
}

/**
 * 
 * 下拉菜单接口
 */

// 获取会员信息
export function getMembersInfo(){
    return get('user/userCheckVipPrice', {});
}


/**
* 收藏
*/
// 获取用户当前文章收藏段落
export function getAllUserCollect(userId:number, articleId:string){
    return get('/collect/getParagraphMarks', {userId, articleId});
}

// 获取用户收藏夹
export function getUserFavorites(userId:number){
    return get('/collect/getUserFavorites', {userId});
}

// 点击收藏
export function collectParagraphInfo(classId:number, userId:number, articleId:string, content:string, indexId:string, entity:string, collectType:string){
    return post('/collect/collectParagraphInfo', {classId, userId, articleId, content, indexId, entity, collectType});
}

// 取消收藏
export function deleteCollection(userId:number, articleId:string, indexId:string, collectType:string, content?:string){
    return post('/collect/deleteUserCollection', {userId, articleId, indexId, collectType, content});
} 

// 增加用户收藏夹
export function addUserFavorites(className:string, userId:number){
    return post('/collect/addUserFavorites', {className, userId});
}

// 删除收藏夹
export function deleteUserFavorites(className:string, userId:number){
    return get('/collect/deleteUserFavorites', {className, userId});
}

// 获取某个收藏夹的收藏信息
export function getFavoriteMessage(pageNum:number, pageSize:number, classId:number){
    return post('/collect/checkCollectFavoriteData', {
        pageNum, 
        pageSize, 
        data:{
            classId
        }
    });
}

// 修改收藏夹名称
export function modifyFavorite(className:string, classId:number){
    return post('/collect/updateUserFavoriteName', {className, classId});
}


// 导出excel表格
// export function favoriteExportExcel(entities:any, title:string, pmcId:string, content:string, className:string){
//     return post('/collect/export-excel', {
//         entities,
//         title,
//         pmcId,
//         content,
//         className
//     }, {
//         responseType: 'blob'
//     });
// }
export function favoriteExportExcel(collectionExcelReqDtoList:any){
    return post('/collect/export-excel', {
        collectionExcelReqDtoList
    }, {
        responseType: 'blob'
    });
}