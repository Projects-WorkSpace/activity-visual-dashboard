<script setup lang="ts">
import { DayActivityModel } from '~~/Types/General';

const props = defineProps<{
    day_activity: DayActivityModel;
}>();
const emits = defineEmits<{
    (e: 'updateActivity', id: number, activity: DayActivityModel): void;
    (e: 'pushedActivityToDelete', payload: DayActivityModel): void;
}>();

const points = ref<number>(props.day_activity.points);
const hrs = ref<number>(props.day_activity.hrs);
const mins = ref<number>(props.day_activity.mins);

const selecthrs = ref<boolean>(false);
const selectmins = ref<boolean>(false);

const getHours = (): number[] => {
    let arr = [0];
    for (let i = 1; i <= 10; i++) {
        arr.push(i);
    }
    return arr;
};
const getMinutes = (): number[] => {
    let arr = [0, 5];
    for (let i = 1; i <= 5; i++) {
        arr.push(i * 10);
    }
    return arr;
};
const selectMins = (payload: number): void => {
    props.day_activity.mins = payload;
    selectmins.value = false;
};
const selectHrs = (payload: number): void => {
    props.day_activity.hrs = payload;
    selecthrs.value = false;
};

const closePageToggles = (): void => {
    if (selecthrs || selectmins) {
        selectmins.value = selecthrs.value = false;
    }
};

const deleteThis = (): void => {
    let activity: DayActivityModel = {
        id: props.day_activity.id,
        points: points.value,
        hrs: hrs.value,
        mins: mins.value,
        date: props.day_activity.date,
        childActivity: props.day_activity.childActivity,
    };
    emits('pushedActivityToDelete', activity);
};
</script>
<template>
    <div class="activity-card w-full grid-cols-3 grid sm:grid-cols-4 gap-x-2 bg-gray-50 shadow-sm ring-1 ring-neutral-200 rounded-sm">
        <div class="sm:col-span-2 flex flex-row items-center gap-x-3 px-2 sm:px-4 py-2">
            <div class="flex items-center" @click="deleteThis">
                <input type="checkbox" />
            </div>
            <label :for="day_activity.id.toString()" class="text-base sm:text-base text-gray-800 font-medium capitalize cursor-pointer">
                {{ day_activity.childActivity.activity.name }}
            </label>
        </div>
        <div class="col-span-1 flex flex-row items-center justify-center gap-x-4 border-l border-neutral-200 px-2 sm:px-4 py-2">
            <input
                type="number"
                class="bg-gray-50 border border-gray-200 text-gray-900 text-base text-center rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-300 block w-[90%] sm:w-[80%] py-2 outline-none"
                placeholder="0"
                v-model="day_activity.points"
            />
        </div>
        <div class="col-span-1 flex items-center gap-x-4 border-l border-neutral-200 px-1 sm:px-4 py-2">
            <div class="w-full rounded-md shadow-sm relative flex flex-col sm:flex-row gap-y-1" role="group ">
                <div v-if="selecthrs" class="absolute top-0 right-0 rounded shadow-2xl bg-gray-50 z-20">
                    <ul class="flex flex-row">
                        <li
                            v-for="hr in getHours()"
                            :key="hr"
                            @click="selectHrs(hr)"
                            class="text-sm px-2.5 py-2 hover:bg-gray-200 cursor-pointer"
                        >
                            {{ hr }}
                        </li>
                    </ul>
                </div>
                <button
                    @click="selecthrs = !selecthrs"
                    type="button"
                    class="inline-flex w-full items-center justify-between gap-x-0.5 px-1.5 sm:px-3 py-2 text-sm font-medium text-gray-900 bg-transparent border border-gray-200 rounded-l-md hover:bg-gray-200 focus:bg-gray-200 transition duration-200 relative"
                >
                    <div class="flex flex-row items-center gap-x-1">
                        <span class="text-gray-700 text-base tracking-wide">{{ day_activity.hrs }}</span>
                        <span class="text-xs sm:text-sm text-tomato">hr</span>
                    </div>
                    <svg
                        class="w-2.5 sm:w-3 h-2.5 sm:h-3 ml-0.5 sm:ml-1"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </button>
                <button
                    @click="selectmins = !selectmins"
                    type="button"
                    class="inline-flex w-full items-center justify-between gap-x-0.5 px-1.5 sm:px-3 py-2 text-sm font-medium text-gray-900 bg-transparent border border-gray-200 rounded-r-md hover:bg-gray-200 focus:bg-gray-200 transition duration-200 relative"
                >
                    <div class="flex flex-row items-center gap-x-1">
                        <span class="text-gray-700 text-base tracking-wide">{{ day_activity.mins }}</span>
                        <span class="text-xs sm:text-sm text-green-500">mins</span>
                    </div>
                    <svg
                        class="w-2.5 sm:w-3 h-2.5 sm:h-3 ml-0.5 sm:ml-1"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </button>
                <div v-if="selectmins" class="absolute top-0 right-0 rounded shadow-2xl bg-gray-50 z-30">
                    <ul class="flex flex-row">
                        <li
                            v-for="min in getMinutes()"
                            :key="min"
                            @click="selectMins(min)"
                            class="text-sm px-2.5 py-2 hover:bg-gray-200 cursor-pointer"
                        >
                            {{ min }}
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div @click="closePageToggles" v-if="selectmins || selecthrs" class="z-10 fixed top-0 bottom-0 left-0 right-0 bg-transparent"></div>
    </div>
</template>

<style scoped>
input[type='number']::-webkit-inner-spin-button,
input[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type='checkbox'] {
    @apply w-4 h-4 appearance-none checked:bg-blue-500 checked:border-none checked:after:text-gray-50 bg-gray-100 border border-gray-300 rounded focus:ring-blue-500 focus:ring-2;
    @apply flex items-center justify-center checked:after:content-['\2713'] checked:after:text-xl;
}
.activity-card {
    font-family: 'DM Mono', monospace;
}
</style>
