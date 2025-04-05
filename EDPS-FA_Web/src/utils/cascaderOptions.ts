// 级联选择器状态
export const cascaderOptions = [
    {
        value: "",
        label: "所有"
    },
    {
        value: "1",
        label: "爬虫阶段",
        children: [
            { value: "11", label: "爬虫待开始" },
            { value: "12", label: "爬虫开始" },
            { value: "13", label: "爬虫失败" }
        ]
    },
    {
        value: "2",
        label: "解析阶段",
        children: [
            { value: "21", label: "解析待开始" },
            { value: "22", label: "解析进行中" },
            { value: "23", label: "解析失败" }
    ]
    },
    {
        value: "3",
        label: "识别阶段"
    },
    {
        value: "4",
        label: "渲染阶段",
    },
    {
        value: "5",
        label: "完成"
    }
];