export function collectType(type: string) {
    const lang = localStorage.getItem('lang') || 'en';
    if (lang === 'zh') {
        switch (type) {
            case "选中":
                return "选中";
            case "段落":
                return "段落";
            default:
                return "未知";
        }
    } else {
        switch (type) {
            case "选中":
                return "selective";
            case "段落":
                return "paragraph";
            default:
                return "Unknown";
        }
    }


}