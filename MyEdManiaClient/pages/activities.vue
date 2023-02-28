<script setup lang="ts">
import { ChildModel, DayActivityModel } from 'Types/General';
import { useAuthStore } from '~~/store/user_store';

const config = useRuntimeConfig();
const useAuth = useAuthStore();

definePageMeta({
    layout: 'app',
});

const date = ref<string>(new Date().toISOString().slice(0, 10));
const selectchild = ref<boolean>(false);
const selecttimechoice = ref<boolean>(false);
const closePageToggles = (): void => {
    if (selectchild || selecttimechoice) {
        selecttimechoice.value = selectchild.value = false;
    }
};

const daily_activities = ref<DayActivityModel[]>([]);
const fetchChildDayActivities = async (): Promise<void> => {
    loadingactivities.value = true;
    const response = await fetch(`${config.public.apiBase}/api/day-activity?date=${date.value}&childID=${selectedchild.value?.id}`, {
        method: 'GET',
    });
    if (response.status === 200) {
        let data = await response.json();
        daily_activities.value = data;
        console.log(daily_activities.value);
        return;
    } else if (response.status === 202) {
        let data = await response.json();
        daily_activities.value = [];
        for (let i = 0; i < data.length; i++) {
            daily_activities.value.push({
                id: Math.floor(Math.random() * (-1 - 100 + 1) + -100),
                points: 0,
                hrs: 0,
                mins: 0,
                date: date.value,
                childActivity: data[i],
            });
        }
        console.log(daily_activities.value);
    } else {
        daily_activities.value = [];
        console.log('Error fetching child activities');
    }
};

const children = ref<ChildModel[]>([]);
const selectedchild = ref<ChildModel | null>(null);
const chooseChild = (payload: ChildModel): void => {
    if (selectedchild.value?.id === payload.id) {
        closePageToggles();
        return;
    }
    selectedchild.value = payload;
    // fetchChildDayActivities();
    closePageToggles();
    setTimeout(() => {
        loadingactivities.value = false;
    }, 600);
};

watch(selectedchild, (newSelectedChild) => {
    console.log('watch Selected child: ', newSelectedChild);
    fetchChildDayActivities();
    setTimeout(() => {
        loadingactivities.value = false;
    }, 600);
});
watch(date, (newDate) => {
    console.log('watch Selected child: ', newDate);
    fetchChildDayActivities();
    setTimeout(() => {
        loadingactivities.value = false;
    }, 600);
});

const loading_child = ref<boolean>(true);
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
    // setTimeout(async () => {
    // });
});

const savingactivity = ref<boolean>(false);
const saveAllActivities = (): void => {
    savingactivity.value = true;
    submitToSaveAllDayActivities();
    setTimeout(() => {
        savingactivity.value = false;
        showActivityMessage();
    }, 600);
};
const updateActivity = (id: number, activity: DayActivityModel) => {
    for (let i = 0; i < daily_activities.value.length; i++) {
        if (daily_activities.value[i].id === id) {
            daily_activities.value[i] = activity;
            break;
        }
    }
};

interface SaveCleanDayData {
    childID: number;
    activityID: number;
    points: number;
    hrs: number;
    mins: number;
    date: string;
}

const submitToSaveAllDayActivities = async (): Promise<void> => {
    let save_data: SaveCleanDayData[] = [];
    for (let i = 0; i < daily_activities.value.length; i++) {
        save_data.push({
            childID: selectedchild.value?.id as number,
            points: daily_activities.value[i]?.points,
            hrs: daily_activities.value[i]?.hrs,
            mins: daily_activities.value[i]?.mins,
            date: date.value,
            activityID: daily_activities.value[i]?.childActivity.activity.id,
        });
    }
    const { data: saved_data, error } = await useFetch(`${config.public.apiBase}/api/post-all-day-activity`, {
        method: 'POST',
        body: save_data,
    });
    if (error.value !== null) {
        console.log(error.value);
        return;
    } else {
        daily_activities.value = (await saved_data.value) as DayActivityModel[];
        // console.log('ID used to save: ', selectedchild.value?.id);
        console.log('Data Saved: ', save_data);
        console.log('Response: ', saved_data.value);
    }
};

const addchildrenmodal = ref<boolean>(false);

const loadingactivities = ref<boolean>(false);

const fetchChildActivities = (): void => {
    loadingactivities.value = true;
    setTimeout(() => {
        loadingactivities.value = false;
    }, 600);
};

// On App Launched fetch user details
onMounted(() => fetchChildActivities());

//
const activitymessage = ref<boolean>(false);
const addnewactivity = ref<boolean>(false);
const showActivityMessage = (): void => {
    activitymessage.value = true;
    setTimeout(() => {
        activitymessage.value = false;
    }, 2000);
};

// Add to fetched list
const updateChildrenList = (child: ChildModel): void => {
    console.log('Saved Child: ', child);
    children.value.push(child);
};
const saveactivity = ref<boolean>(false);

// Emits

// Day Activity Deletion
const activities_todelete = ref<DayActivityModel[]>([]);
const confirm_delete = ref<boolean>(false);

const pushedActivityToDelete = (payload: DayActivityModel): void => {
    for (let i = 0; i < activities_todelete.value.length; i++) {
        if (payload.id === activities_todelete.value[i].id) {
            activities_todelete.value.splice(i, 1);
            return;
        }
    }
    activities_todelete.value.push(payload);
    console.log('Act to be deleted: ', activities_todelete.value);
};

const proceedToDeleteChildActivities = (): void => {
    if (activities_todelete.value.length === 0) {
        return;
    }
    confirm_delete.value = true;
};
const deleting_status = ref<boolean>(false);
const deleteChildActivities = async (): Promise<void> => {
    deleting_status.value = true;
    let idstodelete: any[] = [];
    for (let i = 0; i < activities_todelete.value.length; i++) {
        idstodelete.push({
            childActivityID: activities_todelete.value[i].childActivity.id,
        });
    }
    const { data, error } = await useFetch(`${config.public.apiBase}/api/delete-child-activities`, {
        method: 'DELETE',
        body: idstodelete,
    });
    if (error.value) {
        console.log('Error Deleting this ids');
    } else {
        for (let i = 0; i < activities_todelete.value.length; i++) {
            for (let j = 0; j < daily_activities.value.length; j++) {
                if (daily_activities.value[j].id === activities_todelete.value[i].id) {
                    daily_activities.value.splice(j, 1);
                }
            }
        }
        setTimeout(() => {
            deleting_status.value = false;
            confirm_delete.value = false;
        }, 400);
    }
};

// Activities Update

const pushNewActivities = (payload: DayActivityModel[]): void => {
    saveactivity.value = true;
    for (let i = 0; i < payload.length; i++) {
        daily_activities.value.push(payload[i]);
    }
    addnewactivity.value = !addnewactivity.value;
    setTimeout(() => {
        saveactivity.value = false;
    }, 2000);
};
</script>
<template>
    <section class="w-full flex flex-col">
        <main class="w-full flex flex-col gap-y-4 sm:gap-y-6 px-2 sm:px-4 md:px-14 lg:px-28 xl:px-56 mt-6 sm:mt-8 pb-12">
            <h3 class="text-2xl sm:text-4xl text-gray-800 font-semibold text-center">Daily Activities</h3>
            <!-- <LayoutsDashboardBanner /> -->
            <div
                id="activity-dashboard"
                class="w-full flex flex-col lg:flex-row justify-between gap-y-4 py-3 px-4 border rounded-md border-neutral-200 bg-white"
            >
                <div class="flex flex-col sm:flex-row gap-x-2 gap-y-4 sm:justify-between sm:items-center relative">
                    <div class="flex flex-row items-center gap-x-2">
                        <!-- <h5 class="text-base sm:text-lg tracking-wide text-gray-600 font-serif capitalize hidden sm:block">child:</h5> -->
                        <div class="flex flex-row items-center w-full sm:w-auto relative">
                            <button
                                @click="selectchild = !selectchild"
                                type="button"
                                class="py-2 pl-2 sm:pl-4 pr-4 sm:pr-8 w-full text-base font-normal text-gray-800 focus:outline-none bg-white rounded border border-gray-200 hover:border-gray-300 flex flex-row gap-x-3 items-center relative focus:ring-4 focus:ring-gray-200 transition duration-200"
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
                    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-x-2 gap-y-4">
                        <button
                            @click="addchildrenmodal = !addchildrenmodal"
                            type="button"
                            class="py-2 px-3 sm:px-5 text-base font-medium text-gray-800 flex flex-row items-center gap-x-2 focus:outline-none bg-white rounded-sm border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:ring-4 focus:ring-gray-200 transition duration-200"
                        >
                            <svg
                                class="w-5 h-5 text-gray-600"
                                aria-hidden="true"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z"
                                ></path>
                            </svg>
                            Add new child
                        </button>
                        <button
                            @click="addnewactivity = !addnewactivity"
                            type="button"
                            class="py-2 px-3 sm:px-5 text-base font-medium text-gray-800 flex flex-row items-center gap-x-2 focus:outline-none bg-white rounded-sm border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:ring-4 focus:ring-gray-200 transition duration-200"
                        >
                            <svg
                                class="w-5 h-5 text-gray-600"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="1.5"
                                viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg"
                                aria-hidden="true"
                            >
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15"></path>
                            </svg>
                            Add new activity
                        </button>
                    </div>
                </div>
                <div class="flex flex-row gap-x-2 lg:justify-center items-center relative">
                    <!-- <h5 class="text-sm sm:text-lg tracking-wide text-gray-600 font-serif capitalize hidden sm:block">date:</h5> -->
                    <div class="relative flex items-center w-full">
                        <label for="activity-date" class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
                            <svg
                                aria-hidden="true"
                                class="w-5 h-5 text-gray-500 dark:text-gray-400"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fill-rule="evenodd"
                                    d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                                    clip-rule="evenodd"
                                ></path>
                            </svg>
                        </label>
                        <input
                            id="activity-date"
                            type="date"
                            class="bg-gray-50 border border-gray-300 text-gray-800 tracking-wide text-sm rounded focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2 focus:outline-none transition duration-200"
                            placeholder="Select date"
                            v-model="date"
                        />
                    </div>
                </div>
            </div>
            <div id="container-activities" class="w-full flex flex-col gap-y-2 mt-2.5 sm:mt-4">
                <div id="activities" class="w-full px-1 py-2.5 flex flex-col gap-y-6">
                    <div
                        id="table-header"
                        class="w-full grid grid-cols-3 sm:grid-cols-4 gap-x-2 bg-gray-50 shadow-sm ring-1 ring-neutral-200 rounded-sm"
                    >
                        <div class="sm:col-span-2 flex items-center gap-x-2 px-2 sm:px-4 py-2 sm:py-3.5">
                            <span class="text-lg sm:text-2xl text-gray-600 tracking-wide font-semibold">Activity</span>
                        </div>
                        <div class="col-span-1 flex items-center gap-x-2 border-l border-neutral-200 px-2 sm:px-4 py-2 sm:py-3.5">
                            <span class="text-lg sm:text-2xl text-gray-600 tracking-wide font-semibold">Points</span>
                        </div>
                        <div
                            class="col-span-1 flex items-center justify-between gap-x-2 border-l border-neutral-200 px-2 sm:px-4 py-2 sm:py-3.5"
                        >
                            <span class="text-lg sm:text-2xl text-gray-600 tracking-wide font-semibold">Duration</span>
                        </div>
                    </div>
                    <Transition mode="out-in">
                        <div v-if="daily_activities.length === 0" class="w-full flex flex-col items-start pb-5 pt-2">
                            <h3 class="text-xl font-semibold text-dark">Activities not found</h3>
                            <p class="text-sm text-gray-500">Sorry, we couldn't find the any activites saved for selected child.</p>
                            <div class="mt-2">
                                <button
                                    @click="addnewactivity = !addnewactivity"
                                    type="button"
                                    class="text-gray-600 bg-gray-200 hover:bg-gray-300 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-base px-5 py-2.5 text-center inline-flex items-center transition duration-200"
                                >
                                    Add new activity
                                    <svg
                                        aria-hidden="true"
                                        class="w-5 h-5 ml-2 -mr-1"
                                        fill="currentColor"
                                        viewBox="0 0 20 20"
                                        xmlns="http://www.w3.org/2000/svg"
                                    >
                                        <path
                                            fill-rule="evenodd"
                                            d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                                            clip-rule="evenodd"
                                        ></path>
                                    </svg>
                                </button>
                            </div>
                        </div>
                        <div v-else class="w-full">
                            <Transition name="activity-suspense" mode="out-in">
                                <SkeletonsActivitySuspense v-if="loadingactivities" />
                                <div v-else class="w-full flex flex-col gap-y-2">
                                    <CardsActivityCard
                                        v-for="activity in daily_activities"
                                        :day_activity="activity"
                                        @update-activity="updateActivity"
                                        @pushed-activity-to-delete="pushedActivityToDelete"
                                        :key="activity.id"
                                    />
                                </div>
                            </Transition>
                        </div>
                    </Transition>
                </div>
                <div v-if="daily_activities.length !== 0" class="w-full flex flex-col items-start gap-y-5 pt-4">
                    <div class="w-full flex flex-row items-start gap-x-4">
                        <button
                            @click="saveAllActivities"
                            type="button"
                            class="text-white bg-blue-700 bg-opacity-90 hover:bg-opacity-100 focus:ring-2 focus:outline-none focus:ring-blue-300 font-medium rounded-md text-base tracking-wide px-8 sm:px-10 py-2.5 text-center inline-flex items-center"
                        >
                            <svg
                                v-if="savingactivity"
                                aria-hidden="true"
                                role="saving_status"
                                class="inline w-4 sm:w-5 h-4 sm:h-5 mr-2 sm:mr-3 text-white animate-spin"
                                viewBox="0 0 100 101"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                    fill="#E5E7EB"
                                />
                                <path
                                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                    fill="currentColor"
                                />
                            </svg>
                            Save
                        </button>
                        <button
                            @click="proceedToDeleteChildActivities"
                            type="button"
                            class="py-2.5 pl-4 pr-8 text-base font-medium text-red-500 focus:outline-none bg-white rounded-lg border border-red-400 transition duration-200 flex items-center"
                            :class="
                                activities_todelete.length === 0
                                    ? 'cursor-not-allowed'
                                    : 'hover:bg-red-500 hover:text-gray-100 focus:ring-2 focus:ring-red-300'
                            "
                        >
                            <svg
                                class="inline w-4 sm:w-5 h-4 sm:h-5 mr-3"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="1.5"
                                viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg"
                                aria-hidden="true"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
                                ></path>
                            </svg>
                            Delete
                        </button>
                    </div>
                    <div class="w-full flex flex-col md:flex-row gap-3 items-start">
                        <p class="text-sm text-gray-400">Update the points or duration columns and click the save button</p>
                        <p class="text-sm hidden md:block text-gray-500">/</p>
                        <p class="text-sm text-gray-400">Click on the checkboxes to select which activity to delete.</p>
                    </div>
                </div>
            </div>
            <div
                @click="closePageToggles"
                v-if="selecttimechoice || selectchild"
                class="fixed top-0 bottom-0 left-0 right-0 bg-transparent"
            ></div>
            <Transition name="modals">
                <div
                    id="modals"
                    v-if="addchildrenmodal || addnewactivity"
                    class="fixed bottom-0 top-0 left-0 right-0 bg-transparent flex flex-col items-center justify-center z-30 bg-gray-300 bg-opacity-40 overflow-y-auto"
                >
                    <ModalsAddChild
                        v-if="addchildrenmodal"
                        @close-modal="addchildrenmodal = !addchildrenmodal"
                        @update-children-list="updateChildrenList"
                    />
                    <ModalsSelectActivity
                        v-if="addnewactivity"
                        @close-modal="addnewactivity = !addnewactivity"
                        :child="selectedchild"
                        :date="date"
                        @push-new-activities="pushNewActivities"
                    />
                </div>
            </Transition>
            <Transition name="toast">
                <div v-if="activitymessage" class="absolute top-2 left-1/2 -translate-x-1/2 z-50">
                    <div
                        id="toast-success"
                        class="flex items-center w-full max-w-xs p-4 mb-4 text-gray-500 bg-white rounded-lg shadow"
                        role="alert"
                    >
                        <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-green-500 bg-green-100 rounded-lg">
                            <svg
                                aria-hidden="true"
                                class="w-5 h-5"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fill-rule="evenodd"
                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                    clip-rule="evenodd"
                                ></path>
                            </svg>
                            <span class="sr-only">Check icon</span>
                        </div>
                        <div class="ml-3 text-sm font-normal truncate">All Activities saved successfully.</div>
                        <button
                            type="button"
                            class="ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8"
                            data-dismiss-target="#toast-success"
                            aria-label="Close"
                        >
                            <span class="sr-only">Close</span>
                            <svg
                                aria-hidden="true"
                                class="w-5 h-5"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fill-rule="evenodd"
                                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                    clip-rule="evenodd"
                                ></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </Transition>
            <div v-if="saveactivity" class="fixed top-2 left-1/2 -translate-x-1/2 z-50">
                <div
                    id="toast-success"
                    class="flex items-center w-full max-w-xs p-4 mb-4 text-gray-500 bg-white rounded-lg shadow"
                    role="alert"
                >
                    <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-green-500 bg-green-100 rounded-lg">
                        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path
                                fill-rule="evenodd"
                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                clip-rule="evenodd"
                            ></path>
                        </svg>
                        <span class="sr-only">Check icon</span>
                    </div>
                    <div class="ml-3 text-sm font-normal truncate">Saved new activity successfully.</div>
                    <button
                        type="button"
                        class="ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8"
                        data-dismiss-target="#toast-success"
                        aria-label="Close"
                    >
                        <span class="sr-only">Close</span>
                        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path
                                fill-rule="evenodd"
                                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                clip-rule="evenodd"
                            ></path>
                        </svg>
                    </button>
                </div>
            </div>
            <Transition name="delete-toast">
                <div v-if="confirm_delete" class="fixed top-0 bottom-0 left-0 right-0 flex items-center justify-center z-20">
                    <div class="relative w-[85vw] sm:w-[400px] h-auto z-20">
                        <div class="relative bg-white rounded-lg shadow">
                            <button
                                @click="confirm_delete = !confirm_delete"
                                type="button"
                                class="absolute top-3 right-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center"
                                data-modal-hide="popup-modal"
                            >
                                <svg
                                    aria-hidden="true"
                                    class="w-5 h-5"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                    xmlns="http://www.w3.org/2000/svg"
                                >
                                    <path
                                        fill-rule="evenodd"
                                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                        clip-rule="evenodd"
                                    ></path>
                                </svg>
                                <span class="sr-only">Close modal</span>
                            </button>
                            <div class="p-6 text-center">
                                <svg
                                    aria-hidden="true"
                                    class="mx-auto mb-4 text-gray-400 w-14 h-14"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                    xmlns="http://www.w3.org/2000/svg"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                                    ></path>
                                </svg>
                                <h3 class="mb-5 text-lg font-normal text-gray-500">
                                    Are you sure you want to delete this Activities permanently?
                                </h3>
                                <button
                                    @click="deleteChildActivities"
                                    data-modal-hide="popup-modal"
                                    type="button"
                                    class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center mr-2 transition duration-200"
                                >
                                    <Transition mode="out-in">
                                        <div role="status" v-if="deleting_status" class="min-w-[5rem]">
                                            <svg
                                                aria-hidden="true"
                                                class="inline w-6 h-6 text-gray-200 animate-spin"
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
                                        <span v-else>Yes, I'm sure</span>
                                    </Transition>
                                </button>
                                <button
                                    @click="confirm_delete = !confirm_delete"
                                    data-modal-hide="popup-modal"
                                    type="button"
                                    class="text-gray-500 bg-white hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 rounded-lg border border-gray-200 text-sm font-medium px-5 py-2.5 hover:text-gray-900 focus:z-10 transition duration-200"
                                >
                                    No, cancel
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </Transition>
            <Transition name="bg-anime">
                <div
                    v-if="confirm_delete"
                    id="background-anime"
                    class="fixed top-0 bottom-0 left-0 right-0 bg-gray-300 opacity-40 z-10"
                ></div>
            </Transition>
        </main>
    </section>
</template>

<style scoped>
#activities::-webkit-scrollbar {
    @apply w-[2px] sm:w-[4px] h-[1px] rounded-[4px];
}

#activities::-webkit-scrollbar-corner {
    @apply bg-gray-300;
}

#activities::-webkit-scrollbar-thumb {
    @apply bg-gray-300 rounded-[4px];
}
#activities::-webkit-scrollbar-track {
    @apply bg-gray-200;
}

.modals-enter-from {
    @apply translate-y-full opacity-0;
}
.modals-enter-active,
.modals-leave-active {
    @apply transition duration-300;
}
.modals-leave-to {
    @apply opacity-0;
}

.toast-enter-from {
    @apply -top-1/4 opacity-0;
}
.toast-enter-active {
    @apply transition duration-300;
}

.delete-toast-enter-from {
    @apply scale-0 opacity-0;
}
.delete-toast-enter-active {
    @apply transition duration-300;
}
.bg-anime-enter-from {
    @apply opacity-0;
}
.bg-anime-enter-active {
    @apply transition duration-500;
}
</style>
