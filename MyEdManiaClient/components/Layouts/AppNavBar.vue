<script setup lang="ts">
import { useAuthStore } from '~/store/user_store';

const accountdropdown = ref<boolean>(false);

const useAuth = useAuthStore();

const logoutUser = (): void => {
    localStorage.removeItem('edmania_user');
    useRouter().push('/users');
};
</script>
<template>
    <nav class="w-full flex flex-col gap-y-2 sticky top-0 bg-cover z-20">
        <div id="top-nav-layer" class="w-full flex flex-row justify-between items-center pt-3 pb-1 px-4 md:px-8 lg:px-20">
            <NuxtLink to="/" class="text-2xl sm:text-2xl font-semibold tracking-wide text-gray-50">
                <img src="~/assets/logo/ed-logo3.webp" alt="" class="w-8 scale-150" />
            </NuxtLink>
            <div class="flex flex-row gap-x-3 items-center relative">
                <div
                    @click="() => (accountdropdown = !accountdropdown)"
                    class="flex flex-row gap-x-1 items-center cursor-pointer hover:opacity-80 transition duration-200"
                >
                    <div class="relative w-8 h-8 overflow-hidden bg-blue-100 rounded-full">
                        <img src="/user.png" alt=" " class="w-full h-full rounded-full" />
                    </div>
                    <svg
                        class="w-4 h-4 text-gray-200"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </div>
                <div
                    v-if="accountdropdown"
                    id="dropdownAvatar"
                    class="bg-white divide-y divide-gray-100 rounded shadow w-44 absolute top-[170%] right-0 z-30"
                >
                    <div class="px-4 py-3 text-sm text-gray-900 dark:text-white">
                        <div class="font-medium truncate">{{ useAuth.authDetails?.emailAddress || 'user' }}</div>
                    </div>
                    <ul class="py-1 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownUserAvatarButton">
                        <li>
                            <NuxtLink to="/" class="block px-4 py-2 hover:bg-gray-100">Home</NuxtLink>
                        </li>
                    </ul>
                    <div class="py-1">
                        <button
                            @click="logoutUser"
                            class="block w-full text-start px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white"
                        >
                            Sign out
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div
            id="bottom-nav-layer"
            class="w-full bg-background border-y border-gray-200 pt-1.5 flex flex-row gap-x-4 sm:gap-x-8 items-center justify-center px-4 md:px-8 lg:px-20"
        >
            <NuxtLink to="/activities">
                <div class="w-4 sm:w-5 h-4 sm:h-5 flex justify-center items-center">
                    <IconsActivity />
                </div>
                Activities
            </NuxtLink>
            <NuxtLink to="/reports">
                <div class="w-4 sm:w-5 h-4 sm:h-5 flex justify-center items-center">
                    <IconsReport />
                </div>
                Reports
            </NuxtLink>
        </div>
        <div
            v-if="accountdropdown"
            @click="accountdropdown = false"
            id="body-toggle-auth"
            class="fixed top-0 bottom-0 left-0 right-0 bg-transparent z-20"
        ></div>
    </nav>
</template>

<style scoped>
#bottom-nav-layer a {
    @apply py-2 px-5 mb-1.5 text-sm sm:text-base font-medium text-gray-900 flex flex-row items-center gap-x-2 focus:outline-none bg-white rounded-full border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 transition duration-200;
}
#bottom-nav-layer .activeClass {
    @apply bg-gray-100 text-blue-700;
}
</style>
