export interface tableRow {
    articleJson: string,
    articleType: string,
    author: string,
    createTime: string,
    endTime: string,
    excelPath: string,
    excelUrl: string,
    htmlPath: string,
    htmlUrl: string,
    id: string,
    info: string,
    pdfCompletion: string,
    pdfOssUrl: string,
    pdfPath: string,
    pdfPubmedUrl: string
    pdfSpiderUrl: string,
    pmcId: string,
    startTime: string,
    state: string,
    submitType: string,
    templateBigId: string,
    templateBigName: string,
    title: string,
    updateTime: string,
    userId: string,
    version: string,
    visible: string,
    zipPath: string,
    zipUrl: string,
}

export interface ReceivedFromHtml {
    content: string,
    pmid: string,
    pmcid: string,
    paragraphId: string,
    isCollected: boolean,
    collectType: string,
    mouseX:number,
    mouseY:number,
    entities: Array<{
        name: string,
        type: string,
        typeName: string
    }>
}