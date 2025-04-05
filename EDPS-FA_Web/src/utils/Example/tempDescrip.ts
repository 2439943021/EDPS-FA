export const getTemplateType = (tempType: string) => {
    const lang = localStorage.getItem('lang') || 'zh';
    if (lang === 'zh') {
        switch (tempType) {
            case "0":
                return { label: "基础" };
            case "1":
                return { label: "私人" };
            case "2":
                return { label: "公共" };
        }
    } else {
        switch (tempType) {
            case "0":
                return { label: "Basic" }; // 基础 -> Basic
            case "1":
                return { label: "Private" }; // 私人 -> Private
            case "2":
                return { label: "Public" }; // 公共 -> Public
        }
    }

}