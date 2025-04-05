// 存储每个状态的剩余时间（确保时间每秒递减）
let stateTimeRemaining: Record<string, number> = {};
let timers: Record<string, NodeJS.Timeout> = {}; // 用于存储每个状态的定时器

// 定义状态的最低时间
const stateMinTime: Record<string, number> = {
    "00": 8,
    "0": 8,
    "1": 8,
    "11": 8,
    "12": 8,
    "13": 0,
    "2": 6,
    "21": 6,
    "22": 6,
    "23": 0,
    "3": 4,
    "31": 4,
    "32": 4,
    "33": 0,
    "4": 2,
    "41": 2,
    "42": 2,
    "43": 0,
    "5": 0,
    "51": 0,
};

// 获取随机时间
function getRandomInt(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// 获取一个随机递减值，范围是 minDecrement 到 maxDecrement
function getRandomDecrement(minDecrement: number, maxDecrement: number): number {
    return getRandomInt(minDecrement, maxDecrement);
}

// 初始化各个状态的时间范围
export const getStateTime = (stateCode: string) => {
    // 如果该状态没有初始时间，则设置初始时间
    if (!(stateCode in stateTimeRemaining)) {
        let time = 0;
        switch (stateCode) {
            case "00":
            case "0":
                time = getRandomInt(7, 8); // 随机时间在240到260秒之间
                break;
            case "1":
            case "11":
            case "12":
                time = getRandomInt(6, 8); // 随机时间在180到220秒之间
                break;
            case "13":
                time = 0; 
                break;
            case "2":
            case "21":
            case "22":
                time = getRandomInt(4, 6); // 随机时间在160到200秒之间
                break;
            case "23":
                time = 0; // 时间为 0
                break;
            case "3":
            case "31":
            case "32":
                time = getRandomInt(2, 6); // 随机时间在140到180秒之间
                break;
            case "33":
                time = 0; // 时间为 0
                break;
            case "4":
            case "41":
            case "42":
                time = getRandomInt(1, 2); // 随机时间在100到150秒之间
                break;
            case "43":
                time = 0; // 时间为 0
                break;
            case "5":
            case "51":
                time = 0; // 完成状态时间为0
                break;
            default:
                time = 0;
        }

        // 确保生成的时间不低于最低时间
        if (stateMinTime[stateCode] !== undefined && time < stateMinTime[stateCode]) {
            time = stateMinTime[stateCode]; // 重置为最低时间
        }

        // 初始化该状态的剩余时间
        stateTimeRemaining[stateCode] = time;

        // 如果状态的剩余时间大于 0，则启动定时器来每秒递减时间
        if (time > 0) {
            // 防止多个定时器并行
            if (timers[stateCode]) {
                clearInterval(timers[stateCode]);
            }
            // 启动定时器每秒递减剩余时间
            timers[stateCode] = setInterval(() => {
                if (stateTimeRemaining[stateCode] > 0) {
                    // 随机递减时间（最小递减1秒，最大递减5秒）
                    const decrement = getRandomDecrement(1,2);  // 递减值在 1 到 5 之间
                    stateTimeRemaining[stateCode] -= decrement;
                    if (stateTimeRemaining[stateCode] < 0) {
                        stateTimeRemaining[stateCode] = 0; // 防止时间为负值
                    }
                } else {
                    // 如果时间已达到 0，则清除定时器
                    clearInterval(timers[stateCode]);
                    timers[stateCode] = undefined;
                }
            }, 1000); // 每秒递减
        }
    }

    // 获取当前状态的剩余时间
    let time = stateTimeRemaining[stateCode];

    // 如果剩余时间小于最低时间，强制设置为最低时间
    if (stateMinTime[stateCode] !== undefined && time < stateMinTime[stateCode]) {
        time = stateMinTime[stateCode];
        stateTimeRemaining[stateCode] = time;  // 更新剩余时间为最低时间
    }

    return { time }; // 返回递减后的时间
};
