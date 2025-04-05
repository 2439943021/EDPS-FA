export interface OutputCollects {
    entities: [{
        name: string,
        type: string
    }],
    className: string,
    pmcId: string,
    title: string,
    content: string,
    collectType:string
}

export interface Collects {
    author: string,
    classId: number,
    htmlUrl: string,
    id: string,
    entity:string,
    indexId: string,
    entities: string,
    className: string,
    pmcId: string,
    title: string,
    content: string
}

export interface TableData {
    author: string,
    content: string,
    htmlUrl: string,
    pmcId: string,
    title: string,
}

export interface Favorities {
    className: string;
    classId: number;
    userId: number;
    index: string;
}