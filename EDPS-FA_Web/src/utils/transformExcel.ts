import { ElMessage } from 'element-plus'
import * as XLSX from 'xlsx'
export const transformExcel = (f: Blob) => {
    return new Promise((resolve) => {
        const reader = new FileReader()
        reader.onload = e => {
            let data: unknown = []
            const { result } = e.target
            try {
                // 以二进制流读取整份Excel表格对象
                const workbook = XLSX.read(result, { type: 'binary' })
                // 遍历工作表进行读取（默认是第一张表）
                for (const sheet in workbook.Sheets) {
                    if (workbook?.Sheets?.hasOwnProperty(sheet)) {
                        // 处理好的数据
                        data = data.concat(XLSX.utils.sheet_to_json(workbook.Sheets[sheet]))
                    }
                }
            } catch (err) {
                ElMessage.error('文件类型不正确')
                return
            }
            // 最终的结果
            resolve(data)
        }
        // 以二进制的方式打开
        reader.readAsBinaryString(f)
    })
}