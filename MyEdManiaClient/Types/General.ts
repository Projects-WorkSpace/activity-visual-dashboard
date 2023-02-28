export interface Child {
    id: number;
    name: string;
}

export interface ChildModel {
    id: number;
    name: string;
    dateOfBirth: string;
}

export interface ActivityModel {
    id: number;
    name: string;
}

export interface DayActivityModel {
    id: number;
    points: number;
    hrs: number;
    mins: number;
    date: string;
    childActivity: ChildActivity;
}
export interface ChildActivity {
    id: number;
    childID: number;
    enabled: boolean;
    activity: Activity;
}
export interface Activity {
    id: number;
    name: string;
}

export interface ReportModelEntity {
    id: number;
    points: number;
    date: string;
    duration: number;
    weekday: string;
    activityName: string;
}
export type DayReportModel = ReportModelEntity[];

export type WeekReportModel = DayReportModel[];

export interface ArrangedReportsModel {
    activity: string;
    points: number[];
    duration: number[];
}

export interface PointSeries {
    name: string;
    type: string;
    data: number[];
    smooth: boolean;
}

export interface DurationSeries {
    name: string;
    type: string;
    data: number[];
    smooth: boolean;
}
