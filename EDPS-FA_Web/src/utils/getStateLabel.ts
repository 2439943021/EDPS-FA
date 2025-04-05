// 生成一个介于min（包括）和max（不包括）之间的随机整数
function getRandomInt(min: number, max: number) {
    return Math.floor(Math.random() * (max - min)) + min;
}
export const getStateLabel = (stateCode: string) => {
    // 根据 stateCode 返回对应的状态
    const lang = localStorage.getItem('lang') || 'en';
    if (lang === 'zh') {
        switch (stateCode) {
            case "00":
            case "0":
                return { label: "待开始", color: "#800000", progress: 0 }; // 待爬虫状态的文字颜色为红色
            case "1":
                return { label: "爬虫阶段", color: "#000080", progress: 20 };
            case "11":
                return { label: "准备采集开源数据", color: "#000080", progress: 20 }; // 开始爬虫状态的文字颜色为绿色
            // return { label: $t('messages.editDelete'), color: "#000080", progress:20};
            case "12":
                // return { label: "爬虫开始 ", color: "#000080", progress:20}; // 开始解析状态的文字颜色为蓝色
                return { label: "采集开源数据中", color: "#000080", progress: 20 };
            case "13":
                return { label: "来源无下载链接，无法采集该开源PDF", color: "#000080", progress: 20 }; // 开始识别状态的文字颜色为黄色
            case "2":
                return { label: "解析阶段", color: "#808000", progress: 40 };
            case "21":
                return { label: "解析待开始", color: "#808000", progress: 40 }; // 开始生成 HTML 状态的文字颜色为品红色
            case "22":
                return { label: "解析进行中", color: "#808000", progress: 40 }; // 完成状态的文字颜色为黑色
            case "23":
                return { label: "解析失败", color: "#808000", progress: 40 }; // 完成状态的文字颜色为黑色
            case "3":
                return { label: "识别阶段", color: "#000000", progress: 60 };
            case "31":
                return { label: "识别待开始", color: "#000000", progress: 60 }; // 完成状态的文字颜色为黑色
            case "32":
                return { label: "识别进行中", color: "#000000", progress: 60 }; // 完成状态的文字颜色为黑色
            case "33":
                return { label: "识别失败 ", color: "#000000", progress: 60 }; // 完成状态的文字颜色为黑色
            case "4":
                return { label: "渲染阶段", color: "#800080", progress: 60 };
            case "41":
                return { label: "渲染待开始", color: "#800080", progress: 60 }; // 完成状态的文字颜色为黑色
            case "42":
                return { label: "渲染进行中", color: "#800080", progress: 60 }; // 完成状态的文字颜色为黑色
            case "43":
                return { label: "渲染失败", color: "#800080", progress: 60 }; // 完成状态的文字颜色为黑色
            case "5":
                return { label: "完成", color: "#67C23A", progress: 100 };
            case "51":
                return { label: "完成", color: "#67C23A", progress: 100 }; // 完成状态的文字颜色为黑色    
            default:
                return { label: "所有", color: "", progress: 0 }; // 其他状态的文字颜色为空
        }
    } else {
        switch (stateCode) {
            case "00":
            case "0":
                return { label: "Pending", color: "#800000", progress: 0 }; // Pending (待开始)
            case "1":
                return { label: "Crawling Stage", color: "#000080", progress: 20 }; // Crawling Stage (爬虫阶段)
            case "11":
                return { label: "Preparing to Collect Open Source Data", color: "#000080", progress: 20 }; // Preparing to Collect Open Source Data (准备采集开源数据)
            case "12":
                return { label: "Collecting Open Source Data", color: "#000080", progress: 20 }; // Collecting Open Source Data (采集开源数据中)
            case "13":
                return { label: "No Download Link, Cannot Collect PDF", color: "#000080", progress: 20 }; // No Download Link, Cannot Collect PDF (来源无下载链接，无法采集该开源PDF)
            case "2":
                return { label: "Parsing Stage", color: "#808000", progress: 40 }; // Parsing Stage (解析阶段)
            case "21":
                return { label: "Parsing Pending", color: "#808000", progress: 40 }; // Parsing Pending (解析待开始)
            case "22":
                return { label: "Parsing In Progress", color: "#808000", progress: 40 }; // Parsing In Progress (解析进行中)
            case "23":
                return { label: "Parsing Failed", color: "#808000", progress: 40 }; // Parsing Failed (解析失败)
            case "3":
                return { label: "Recognition Stage", color: "#000000", progress: 60 }; // Recognition Stage (识别阶段)
            case "31":
                return { label: "Recognition Pending", color: "#000000", progress: 60 }; // Recognition Pending (识别待开始)
            case "32":
                return { label: "Recognition In Progress", color: "#000000", progress: 60 }; // Recognition In Progress (识别进行中)
            case "33":
                return { label: "Recognition Failed", color: "#000000", progress: 60 }; // Recognition Failed (识别失败)
            case "4":
                return { label: "Rendering Stage", color: "#800080", progress: 60 }; // Rendering Stage (渲染阶段)
            case "41":
                return { label: "Rendering Pending", color: "#800080", progress: 60 }; // Rendering Pending (渲染待开始)
            case "42":
                return { label: "Rendering In Progress", color: "#800080", progress: 60 }; // Rendering In Progress (渲染进行中)
            case "43":
                return { label: "Rendering Failed", color: "#800080", progress: 60 }; // Rendering Failed (渲染失败)
            case "5":
                return { label: "Completed", color: "#67C23A", progress: 100 }; // Completed (完成)
            case "51":
                return { label: "Completed", color: "#67C23A", progress: 100 }; // Completed (完成)
            default:
                return { label: "All", color: "", progress: 0 }; // All (所有)
        }

    }

}
/*
export const getStateLabel = (stateCode: string) => {
    // 根据 stateCode 返回对应的状态
    switch (stateCode) {
        case "00":
        case "0":
            return { label: "未完成", color: "#000080", progress:0}; 
        case "1":
            return { label: "未完成", color: "#000080", progress:getRandomInt(1,21) };
        case "11":
            return { label: "未完成", color: "#000080", progress:getRandomInt(1,21) };  
        case "12":
            return { label: "未完成 ", color: "#000080", progress:getRandomInt(1,21) }; 
        case "13":
            return { label: "未完成", color: "#000080", progress:getRandomInt(1,21) }; 
        case "2":
            return { label: "未完成", color: "#000080", progress:getRandomInt(21,41) };
        case "21":
            return { label: "未完成", color: "#000080", progress:getRandomInt(21,41) }; 
        case "22":
            return { label: "未完成", color: "#000080", progress:getRandomInt(21,41) }; 
        case "23":
            return { label: "未完成", color: "#000080", progress:getRandomInt(21,41) }; 
        case "3":
            return { label: "未完成", color: "#000080", progress:getRandomInt(41,61) };   
        case "31":
            return { label: "未完成", color: "#000080", progress:getRandomInt(41,61) }; 
        case "32":
            return { label: "未完成", color: "#000080", progress:getRandomInt(41,61) }; 
        case "33":
            return { label: "未完成 ", color: "#000080", progress:getRandomInt(41,61) }; 
        case  "4":
            return { label: "未完成", color: "#000080", progress:getRandomInt(61,81) };
        case "41":
            return { label: "未完成", color: "#000080", progress:getRandomInt(61,81) }; 
        case "42":
            return { label: "未完成", color: "#000080", progress:getRandomInt(61,81) }; 
        case "43":
            return { label: "未完成", color: "#000080", progress:getRandomInt(61,81) }; 
        case "5":
            return { label: "完成", color: "#67C23A", progress:100 };
        case "51":
            return { label: "完成", color: "#67C23A", progress:100 }; // 完成状态的文字颜色为绿色   
        default:
            return { label: "所有", color: "",  progress:0 }; // 其他状态的文字颜色为空
    }
}
*/
// 查看报告中不同的提交方式
export const getSubmitType = (submitType: string) => {
    switch (submitType) {
        case "01":
            return { label: "Pmid" }
        case "02":
            return { label: "Excel" }
        case "03":
            return { label: "Pdf" }
    }
}

