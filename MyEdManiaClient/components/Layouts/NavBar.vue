<script setup lang="ts">
const mobiletoggle = ref<boolean>(false);
</script>
<template>
    <div class="w-full grid grid-cols-2 sm:grid-cols-3 bg-cover px-5 sm:px-8 lg:px-20 xl:px-40 py-4 sm:py-5">
        <div class="col-span-1 flex flex-row items-center">
            <NuxtLink to="/" class="text-2xl sm:text-2xl font-semibold tracking-wide text-gray-50">
                <img src="~/assets/logo/ed-logo3.webp" alt="" class="w-10 scale-150" />
            </NuxtLink>
        </div>
        <div id="left-nav" class="col-span-1 sm:col-span-2 text-gray-100">
            <div class="w-full hidden sm:flex flex-row gap-x-4 sm:gap-x-8 justify-end items-center">
                <NuxtLink to="/activities">
                    <div class="w-5 h-5 flex justify-center items-center">
                        <IconsActivity />
                    </div>
                    <span>Activities</span>
                </NuxtLink>
                <NuxtLink to="/reports">
                    <div class="w-5 h-5 flex justify-center items-center">
                        <IconsReport />
                    </div>
                    <span>Reports</span>
                </NuxtLink>
                <div id="authBtns" class="flex flex-row gap-x-2 items-center">
                    <button
                        @click="useRouter().push('/users')"
                        type="button"
                        class="e border border-gray-300 focus:outline-none bg-opacity-80 hover:bg-opacity-100 focus:bg-opacity-100 focus:ring-2 focus:ring-gray-200 font-medium rounded-md text-sm sm:text-base px-3 sm:px-6 py-1.5"
                    >
                        Log In
                    </button>
                </div>
            </div>
            <div id="mobile-view" class="w-full flex sm:hidden flex-row gap-x-4 sm:gap-x-8 justify-end items-center px-1">
                <button
                    @click="mobiletoggle = !mobiletoggle"
                    type="button"
                    class="inline-flex items-center p-1 text-sm text-gray-50 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 hover:text-gray-800 focus:text-gray-800 transition duration-200"
                >
                    <span class="sr-only">Open main menu</span>
                    <svg aria-hidden="true" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path
                            fill-rule="evenodd"
                            d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                            clip-rule="evenodd"
                        ></path>
                    </svg>
                </button>
            </div>
        </div>
        <Transition name="drop-down">
            <div
                v-if="mobiletoggle"
                id="mobile-drop-down"
                class="fixed top-0 bottom-0 left-0 right-0 bg-cover bg-opacity-90 z-10 flex sm:hidden flex-col items-center justify-center"
            >
                <button
                    @click="mobiletoggle = !mobiletoggle"
                    type="button"
                    class="absolute right-5 top-5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8"
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
                <div class="grid grid-cols-1 gap-y-8">
                    <NuxtLink to="/activities" class="flex flex-row gap-x-2 items-center text-gray-50 text-4xl font-semibold">
                        <div class="w-10 h-10 flex justify-center items-center">
                            <IconsActivity />
                        </div>
                        <span>Activities</span>
                    </NuxtLink>
                    <NuxtLink to="/reports" class="flex flex-row gap-x-2 items-center text-gray-50 text-4xl font-semibold">
                        <div class="w-10 h-10 flex justify-center items-center">
                            <IconsReport />
                        </div>
                        <span>Reports</span>
                    </NuxtLink>
                    <NuxtLink to="/users" class="flex flex-row gap-x-2 items-center text-gray-50 text-4xl font-semibold">
                        <div class="w-10 h-10 flex justify-center items-center">
                            <IconsLogin />
                        </div>
                        <span>Login</span>
                    </NuxtLink>
                </div>
            </div>
        </Transition>
    </div>
</template>

<style scoped>
#left-nav a {
    @apply text-sm sm:text-lg tracking-wide hidden sm:flex flex-row items-center gap-x-2 capitalize font-light;
}

.drop-down-enter-from,
.drop-down-leave-to {
    @apply -translate-y-full opacity-0;
}
.drop-down-enter-active,
.drop-down-leave-active {
    @apply transition duration-300;
}
</style>
