<script setup lang="ts">
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import { ChildModel, WeekReportModel, ArrangedReportsModel, PointSeries, DurationSeries } from 'Types/General';
import { useAuthStore } from '~~/store/user_store';

definePageMeta({
    layout: 'app',
});

const config = useRuntimeConfig();
const useAuth = useAuthStore();
const children = ref<ChildModel[]>([]);

const fetched_data_status = ref<boolean>(false);

// Default week function
const getWeekStartEnd = (): [Date, Date] => {
    var today = new Date();
    var day = today.getUTCDay();
    var date = today.getUTCDate();
    var diff = date - day + (day == 0 ? -6 : 1);
    var weekStart = new Date(today.setUTCDate(diff));
    var weekEnd = new Date(today.setUTCDate(diff + 6));
    return [weekStart, weekEnd];
};

const chosenweek = ref<[Date, Date] | [string, string]>(getWeekStartEnd());

watch(chosenweek, (newChosenWeek) => {
    console.log('choosen week: ', new Date(newChosenWeek?.[0]).toISOString().slice(0, 10));
});
const selectchild = ref<boolean>(false);
const closePageToggles = (): void => {
    if (selectchild) {
        selectchild.value = false;
    }
};

const selectedchild = ref<ChildModel>(children.value[0]);

const chooseChild = (payload: ChildModel): void => {
    selectedchild.value = payload;
    closePageToggles();
    // fetchReportsData();
};
watch(selectedchild, (newSelectedChild) => {
    fetchReportsData();
});

watch(chosenweek, (newChosenWeek) => {
    fetchReportsData();
});
const loading_child = ref<boolean>(false);
const fetchMyChildren = async (): Promise<ChildModel[] | void> => {
    loading_child.value = true;
    const { data: fetched_children, error } = await useFetch<string, ChildModel[]>(`${config.public.apiBase}/api/mychild`, {
        method: 'Get',
        headers: {
            Authorization: useAuth.authDetails?.Authorization || '',
        },
    });
    if (error.value) {
        useRouter().push('/users');
        return;
    } else {
        children.value = (await fetched_children.value) as unknown as ChildModel[];
        selectedchild.value = await children.value[0];
    }
    setTimeout(() => {
        loading_child.value = false;
    }, 800);
};
onMounted(() => {
    if (useAuth.authDetails?.Authorization === undefined) {
        useRouter().push('/users');
    } else {
        fetchMyChildren();
    }
});

// Data to Plot
const fetched_reports = ref<WeekReportModel>([]);
const weekday = ref<string[]>([]);
const activity_names = ref<string[]>([]);
const fetchReportsData = async (): Promise<void> => {
    fetched_data_status.value = false;
    const { data: reports, error } = await useFetch<WeekReportModel>(`${config.public.apiBase}/api/reports-weekly`, {
        method: 'GET',
        query: {
            childID: selectedchild.value.id,
            startDate: new Date(chosenweek.value[0]).toISOString().slice(0, 10),
            endDate: new Date(chosenweek.value[1]).toISOString().slice(0, 10),
        },
    });
    if (error.value) {
        console.log(error.value);
    } else {
        fetched_reports.value = (await reports.value) as WeekReportModel;
        console.log('Fetched reports: ', fetched_reports.value);
        fetched_data_status.value = true;
    }
};

// Monitor & Track to Update changes
const arranged_data = ref<ArrangedReportsModel[]>([]);
watch(fetched_reports, (newFetched_Reports) => {
    console.log('Activities previous: ', activity_names.value);
    weekday.value = [];
    activity_names.value = [];
    let week_list: string[] = [];
    let activity_list: string[] = [];
    for (let i = 0; i < fetched_reports.value.length; i++) {
        for (let j = 0; j < fetched_reports.value[i].length; j++) {
            week_list.push(fetched_reports.value[i][j].weekday);
            activity_list.push(fetched_reports.value[i][j].activityName);
        }
    }
    weekday.value = [...new Set(week_list)];
    activity_names.value = [...new Set(activity_list)];

    arranged_data.value = [];
    for (let i = 0; i < activity_names.value.length; i++) {
        let point_list: number[] = [];
        let duration_list: number[] = [];
        for (let j = 0; j < fetched_reports.value.length; j++) {
            for (let k = 0; k < fetched_reports.value[j].length; k++) {
                if (activity_names.value[i] === fetched_reports.value[j][k].activityName) {
                    point_list.push(fetched_reports.value[j][k].points);
                    duration_list.push(fetched_reports.value[j][k].duration / 60);
                    break;
                }
            }
        }
        arranged_data.value.push({
            activity: activity_names.value[i],
            points: point_list,
            duration: duration_list,
        });
        point_list = [];
        duration_list = [];
    }
    createPointSeriesData();
    createDurationSeriesData();
    console.log('Activities loaded: ', activity_names.value);
});

// Edit Charts Series Data
const points_series = ref<PointSeries[]>([]);
const createPointSeriesData = (): void => {
    points_series.value = [];
    for (let i = 0; i < arranged_data.value.length; i++) {
        points_series.value.push({
            name: arranged_data.value[i].activity,
            type: 'line',
            data: arranged_data.value[i].points,
            smooth: true,
        });
    }
    console.log('Point Series: ', points_series.value);
};

const duration_series = ref<DurationSeries[]>([]);
const createDurationSeriesData = (): void => {
    duration_series.value = [];
    for (let i = 0; i < arranged_data.value.length; i++) {
        duration_series.value.push({
            name: arranged_data.value[i].activity,
            type: 'line',
            data: arranged_data.value[i].duration,
            smooth: true,
        });
    }
    console.log('Duration Series: ', duration_series.value);
};
</script>
<template>
    <section class="w-full flex flex-col">
        <main class="w-full flex flex-col gap-y-4 sm:gap-y-6 px-2 sm:px-4 md:px-14 lg:px-28 xl:px-52 mt-6 sm:mt-8 pb-12">
            <header class="w-full flex flex-col gap-y-2 px-4">
                <h3 class="text-2xl sm:text-4xl text-gray-800 font-semibold text-center">Weekly Activity Reports</h3>
            </header>
            <div
                class="w-full flex flex-col sm:flex-row justify-between sm:items-center gap-x-8 gap-y-4 py-3 px-4 border rounded-md border-neutral-200 shadow-sm bg-gray-50"
            >
                <div class="flex flex-row gap-x-2 sm:justify-center items-center relative">
                    <!-- <h5 class="text-sm sm:text-lg tracking-wide text-gray-600 font-serif capitalize">child:</h5> -->
                    <div class="flex flex-row items-center w-full sm:w-auto relative">
                        <button
                            @click="selectchild = !selectchild"
                            type="button"
                            class="py-1.5 pl-4 pr-10 w-full text-base font-normal text-gray-800 focus:outline-none bg-white rounded border border-gray-200 hover:border-gray-300 focus:border-gray-300 flex flex-row gap-x-3 items-center relative transition duration-200"
                        >
                            <div class="flex flex-col">
                                <Transition mode="out-in">
                                    <div v-if="loading_child" role="status">
                                        <svg
                                            aria-hidden="true"
                                            class="w-5 h-5 mx-3 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                                            viewBox="0 0 100 101"
                                            fill="none"
                                            xmlns="http://www.w3.org/2000/svg"
                                        >
                                            <path
                                                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                                fill="currentColor"
                                            />
                                            <path
                                                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                                fill="currentFill"
                                            />
                                        </svg>
                                        <span class="sr-only">Loading...</span>
                                    </div>
                                    <span v-else class="capitalize tracking-wide truncate">{{
                                        selectedchild?.name || 'No child found'
                                    }}</span>
                                </Transition>
                            </div>
                            <svg
                                class="w-4 h-4 absolute right-2"
                                aria-hidden="true"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </button>
                        <Transition name="dropdownChild">
                            <div
                                v-if="selectchild"
                                id="dropdownChild"
                                class="z-10 bg-white rounded shadow w-[80%] sm:w-44 dark:bg-gray-700 absolute top-full translate-y-2"
                            >
                                <ul class="h-auto py-1 text-gray-700 dark:text-gray-200" aria-labelledby="dropdownUsersButton">
                                    <li
                                        v-for="child in children"
                                        :key="child.id"
                                        @click="chooseChild(child)"
                                        class="flex items-center px-4 py-2 text-sm sm:text-base hover:bg-gray-100 transition-colors duration-200 cursor-pointer"
                                    >
                                        {{ child.name }}
                                    </li>
                                </ul>
                            </div>
                        </Transition>
                    </div>
                </div>
                <div class="flex flex-row gap-x-2 w-full justify-end items-center relative">
                    <!-- <h5 class="text-sm sm:text-lg tracking-wide text-gray-600 font-serif capitalize">week:</h5> -->
                    <Datepicker v-model="chosenweek" week-picker placeholder="Select week" default="true" class="w-full sm:w-auto" />
                </div>
            </div>
            <div id="charts" class="w-full grid grid-cols-1 gap-y-2 overflow-x-auto sm:overflow-x-hidden py-4 px-1.5">
                <h3 class="text-gray-700 tracking-wide text-lg sm:text-xl font-medium text-center">Activity Points Chart</h3>
                <Transition mode="out-in" name="load-chart">
                    <ChartsPointsLineChart
                        v-if="fetched_data_status"
                        :Activities="activity_names"
                        :Weekdays="weekday"
                        :point_series="points_series"
                    />
                    <ChartsSkeletonChart v-else />
                </Transition>
            </div>
            <div id="charts" class="w-full grid grid-cols-1 gap-y-2 overflow-x-auto sm:overflow-x-hidden py-4 px-1.5">
                <h3 class="text-gray-700 tracking-wide text-lg sm:text-xl font-medium text-center">Time Spent on the Activity Chart</h3>
                <Transition mode="out-in" name="load-chart">
                    <ChartsHourLineChart
                        v-if="fetched_data_status"
                        :Activities="activity_names"
                        :Weekdays="weekday"
                        :duration_series="duration_series"
                    />
                    <ChartsSkeletonChart v-else />
                </Transition>
            </div>
        </main>

        <div @click="closePageToggles" v-if="selectchild" class="fixed top-0 bottom-0 left-0 right-0 bg-transparent"></div>
    </section>
</template>

<style scoped>
#chart-container {
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}

#charts::-webkit-scrollbar {
    @apply w-[2px] sm:w-[4px] h-[1px] rounded-[4px];
}

#charts::-webkit-scrollbar-corner {
    @apply bg-gray-300;
}

#charts::-webkit-scrollbar-thumb {
    @apply bg-gray-300 rounded-[4px];
}
#charts::-webkit-scrollbar-track {
    @apply bg-gray-200;
}

.load-chart.enter-from {
    @apply opacity-0;
}
.load-chart.enter-active {
    @apply transition duration-300;
}
</style>
