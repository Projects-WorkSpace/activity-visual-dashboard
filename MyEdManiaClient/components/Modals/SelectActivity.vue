<script lang="ts" setup>
import { ActivityModel, ChildActivity, ChildModel, DayActivityModel } from '~~/Types/General';

const config = useRuntimeConfig();
const props = defineProps<{
    child: ChildModel | null;
    date: string;
}>();
const emits = defineEmits<{
    (e: 'closeModal'): void;
    (e: 'pushNewActivities', payload: DayActivityModel[]): void;
}>();

const activities = ref<ActivityModel[]>([]);

const fetchAllActivities = async (): Promise<void> => {
    const { data: all_activities, error } = await useFetch<ActivityModel[]>(`${config.public.apiBase}/api/activity`, {
        method: 'GET',
    });
    if (error.value) {
        emits('closeModal');
    } else {
        activities.value = all_activities.value as ActivityModel[];
    }
};

const fetching = ref<boolean>(false);

const all_picked = ref<boolean>(false);
const getActivitiesToSelectFrom = async (): Promise<void> => {
    fetching.value = true;
    await fetchAllActivities();
    await fetchChildActivities();
    setTimeout(() => {
        fetching.value = false;
        if (activities.value.length === 0) {
            all_picked.value = true;
        }
    }, 400);
};

getActivitiesToSelectFrom();

const fetchChildActivities = async (): Promise<void> => {
    const { data: child_activities, error } = await useFetch(`${config.public.apiBase}/api/child-activity?childID=${props.child?.id}`, {
        method: 'GET',
    });
    if (error.value) {
        emits('closeModal');
    } else {
        let acts = child_activities.value as ChildActivity[];
        console.log('Already', acts);
        for (let i = 0; i < acts.length; i++) {
            for (let j = 0; j < activities.value.length; j++) {
                if (activities.value[j].id === acts[i].activity.id) {
                    activities.value.splice(j, 1);
                }
            }
        }
    }
};

const selected_activities = ref<ActivityModel[]>([]);

const chooseActivity = (payload: ActivityModel): void => {
    for (let i = 0; i < selected_activities.value.length; i++) {
        if (payload.id === selected_activities.value[i].id) {
            return;
        }
    }
    selected_activities.value.push(payload);
    for (let i = 0; i < activities.value.length; i++) {
        if (activities.value[i].id === payload.id) {
            activities.value.splice(i, 1);
            break;
        }
    }
};
const unChooseActivity = (payload: ActivityModel): void => {
    for (let i = 0; i < activities.value.length; i++) {
        if (payload.id === activities.value[i].id) {
            return;
        }
    }
    activities.value.push(payload);
    for (let i = 0; i < selected_activities.value.length; i++) {
        if (selected_activities.value[i].id === payload.id) {
            selected_activities.value.splice(i, 1);
            break;
        }
    }
};

const posting_new_activities = ref<boolean>(false);
const saveActivities = async (): Promise<void> => {
    if (selected_activities.value.length === 0) {
        return;
    }
    posting_new_activities.value = true;
    let post_data: any[] = [];
    for (let i = 0; i < selected_activities.value.length; i++) {
        post_data.push({
            childID: props.child?.id,
            activityID: selected_activities.value[i].id,
            enabled: true,
        });
    }
    const { data: saved_activities, error } = await useFetch<ChildActivity[]>(`${config.public.apiBase}/api/post-all-child-activity`, {
        method: 'POST',
        body: post_data,
    });
    if (error.value) {
        return;
    } else {
        let saved = saved_activities.value as ChildActivity[];
        let day_activities: DayActivityModel[] = [];
        for (let i = 0; i < saved.length; i++) {
            day_activities.push({
                id: Math.floor(Math.random() * (-1 - 100 + 1) + -100),
                points: 0,
                hrs: 0,
                mins: 0,
                date: props.date,
                childActivity: saved[i],
            });
        }
        emits('pushNewActivities', day_activities);
        setTimeout(() => {
            posting_new_activities.value = false;
        }, 400);
    }
};
</script>
<template>
    <div class="fixed top-0 bottom-0 left-0 right-0 z-10 flex items-center justify-center flex-col">
        <div class="w-[85vw] sm:w-[400px] h-auto bg-white rounded shadow-md flex flex-col pb-2">
            <div class="w-full relative">
                <button
                    @click="emits('closeModal')"
                    type="button"
                    class="absolute top-3 right-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-800 dark:hover:text-white"
                    data-modal-hide="crypto-modal"
                >
                    <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path
                            fill-rule="evenodd"
                            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                            clip-rule="evenodd"
                        ></path>
                    </svg>
                    <span class="sr-only">Close modal</span>
                </button>
                <!-- Modal header -->
                <div class="px-4 py-3 border-b rounded-t flex flex-row gap-x-2 items-center">
                    <div class="w-5 h-5 text-blue-500">
                        <svg
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
                                d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z"
                            ></path>
                        </svg>
                    </div>
                    <h3 class="text-base font-medium text-gray-900 lg:text-xl dark:text-white">Select Activities</h3>
                </div>
            </div>
            <div class="activities w-full flex flex-wrap gap-x-3 gap-y-3 py-3 px-3">
                <Transition mode="out-in">
                    <div v-if="selected_activities.length === 0" class="w-full flex flex-wrap gap-x-3 gap-y-3">
                        <span
                            class="inline-flex items-center px-2 py-1 mr-2 text-sm font-medium text-blue-800 bg-blue-100 rounded dark:bg-blue-900 dark:text-blue-300"
                        >
                            None selected
                        </span>
                    </div>
                    <div v-else class="w-full flex flex-wrap gap-x-3 gap-y-3">
                        <span
                            v-for="act in selected_activities"
                            :key="act.id"
                            @click="unChooseActivity(act)"
                            class="inline-flex items-center px-2 py-1 mr-2 text-sm font-medium text-blue-800 bg-blue-100 rounded dark:bg-blue-900 dark:text-blue-300"
                        >
                            {{ act.name }}
                            <button
                                type="button"
                                class="inline-flex items-center p-0.5 ml-2 text-sm text-blue-400 bg-transparent rounded-sm hover:bg-blue-200 hover:text-blue-900 dark:hover:bg-blue-800 dark:hover:text-blue-300"
                                data-dismiss-target="#badge-dismiss-default"
                                aria-label="Remove"
                            >
                                <svg
                                    aria-hidden="true"
                                    class="w-3.5 h-3.5"
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
                        </span>
                    </div>
                </Transition>
            </div>
            <Transition mode="out-in">
                <div v-if="!all_picked" class="w-full flex flex-wrap gap-x-3 gap-y-3 px-2 py-3 border-t border-gray-200">
                    <div class="w-full px-0.5">
                        <p class="text-sm text-gray-600">Pick from these activities</p>
                    </div>
                    <div class="w-full flex gap-y-3 flex-col">
                        <Transition mode="out-in">
                            <div v-if="fetching" class="w-full flex flex-wrap gap-x-3 gap-y-3 animate-pulse">
                                <button class="bg-gray-200 rounded h-7 w-20"></button>
                                <button class="bg-gray-200 rounded h-7 w-20"></button>
                                <button class="bg-gray-200 rounded h-7 w-20"></button>
                            </div>
                            <div v-else class="flex flex-wrap gap-x-3 gap-y-3 w-full">
                                <span
                                    v-for="activity in activities"
                                    :key="activity.id"
                                    @click="chooseActivity(activity)"
                                    class="bg-gray-100 text-gray-800 text-sm font-medium px-2.5 py-1 rounded border border-gray-200 hover:bg-gray-200 transition duration-200 cursor-pointer"
                                    >{{ activity.name }}</span
                                >
                            </div>
                        </Transition>
                    </div>
                </div>
                <div v-else class="w-full flex flex-col gap-y-2 justify-start items-start border-t border-gray-200 px-2 py-3">
                    <p class="text-sm text-gray-600">Seems like all activities have been assigned to this child.</p>
                    <span
                        class="bg-blue-100 text-blue-800 text-sm font-medium inline-flex items-center pl-1 pr-2.5 py-0.5 rounded border border-blue-400"
                    >
                        <span class="inline-flex items-center p-1 mr-2 text-sm font-semibold text-gray-50 bg-green-500 rounded-full">
                            <svg
                                aria-hidden="true"
                                class="w-3 h-3"
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
                            <span class="sr-only">Icon description</span>
                        </span>
                        <span>All picked</span>
                    </span>
                </div>
            </Transition>
            <div class="w-full flex flex-col gap-y-1 px-2 py-2">
                <p class="text-sm text-gray-600">Hit this save button after picking some activities</p>
                <button
                    @click="saveActivities"
                    type="button"
                    class="text-white bg-gradient-to-r from-cyan-500 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-cyan-300 dark:focus:ring-cyan-800 font-medium rounded-lg tracking-wide text-lg px-5 py-2 text-center flex flex-row items-center justify-center mt-1 transition duration-200"
                >
                    <Transition mode="out-in">
                        <div role="status" v-if="posting_new_activities">
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
                        <span v-else>Save</span>
                    </Transition>
                </button>
            </div>
        </div>
    </div>
</template>
