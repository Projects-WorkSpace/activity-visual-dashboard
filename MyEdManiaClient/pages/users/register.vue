<script setup lang="ts">
import { useAuthStore } from '~/store/user_store';
import { UserDetails } from '~/Types/UserDetails';

const config = useRuntimeConfig();
const useAuth = useAuthStore();
const invalid_details = ref<boolean>(false);
const registrationdetails = ref<{
    email: string;
    password: string;
    confirm_password: string;
}>({ email: '', password: '', confirm_password: '' });

const details_validation = ref<{
    email: boolean;
    password: boolean;
    confirm_password: boolean;
}>({ email: false, password: false, confirm_password: false });

const showpasswords = ref<{
    password: boolean;
    confirmpassword: boolean;
}>({
    password: true,
    confirmpassword: true,
});

const submittingdetails = ref<boolean>(false);

const saveNewChild = (): void => {
    details_validation.value = {
        email: false,
        password: false,
        confirm_password: false,
    };
    if (registrationdetails.value.email === '') {
        details_validation.value.email = true;
        return;
    } else if (registrationdetails.value.password != registrationdetails.value.confirm_password) {
        details_validation.value.confirm_password = true;
        return;
    } else if (registrationdetails.value.password.length <= 6) {
        details_validation.value.password = true;
    } else {
        submittingdetails.value = true;
        fetchLoginAuthorization();
        setTimeout(() => {
            submittingdetails.value = false;
        }, 500);
    }
};

const fetchLoginAuthorization = async (): Promise<void> => {
    const { data: authorization, error } = await useFetch<string, UserDetails>(config.public.apiBase + '/api/register', {
        method: 'Post',
        body: {
            emailAddress: registrationdetails.value.email,
            password: registrationdetails.value.password,
        },
    });
    if (error.value) {
        console.log(error.value);
        invalid_details.value = true;
        return;
    } else {
        localStorage.setItem('edmania_user', JSON.stringify(authorization.value));
        useAuth.updateAuthDetails(authorization.value as unknown as UserDetails);
        useRouter().push('/users/newchild');
    }
};
</script>
<template>
    <main class="w-full flex flex-col items-center justify-center px-2 sm:px-8 lg:px-20 xl:px-40">
        <header class="flex flex-col gap-y-2 w-[88%] sm:w-[70%] md:w-[60%] lg:w-[40%] pt-16">
            <h3 class="text-3xl font-semibold">
                Create <br />
                an account
            </h3>
            <!-- <p class="text-base text-gray-600">Welcome back you've been missed!</p> -->
        </header>
        <div
            v-if="invalid_details"
            id="toast-danger"
            class="flex items-center w-full max-w-xs p-4 mb-4 text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:bg-gray-800 absolute top-2"
            role="alert"
        >
            <div
                class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-red-500 bg-red-100 rounded-lg dark:bg-red-800 dark:text-red-200"
            >
                <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path
                        fill-rule="evenodd"
                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                        clip-rule="evenodd"
                    ></path>
                </svg>
                <span class="sr-only">Error icon</span>
            </div>
            <div class="ml-3 text-sm font-normal">The email address you provided is already in use. Please try to use another one.</div>
            <button
                @click="invalid_details = !invalid_details"
                type="button"
                class="ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700"
                data-dismiss-target="#toast-danger"
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
        <div class="w-full flex flex-col gap-y-6 pt-8 items-center justify-center">
            <div class="relative w-[88%] sm:w-[70%] md:w-[60%] lg:w-[40%] flex items-center flex-col gap-y-1">
                <input
                    type="text"
                    id="mail"
                    class="block px-2.5 pb-2.5 pt-4 w-full text-base text-gray-900 tracking-wide bg-white rounded-lg border border-gray-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                    placeholder=" "
                    v-model="registrationdetails.email"
                />
                <label
                    for="mail"
                    class="absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
                    >Enter Email</label
                >
                <p v-if="details_validation.email" class="mt-1 text-sm text-red-600 dark:text-red-500 text-start w-full">
                    <span class="font-medium">Please</span> enter a valid email.
                </p>
            </div>
            <div class="relative w-[88%] sm:w-[70%] md:w-[60%] lg:w-[40%] flex items-center">
                <input
                    :type="showpasswords.password ? 'password' : 'text'"
                    id="pass"
                    class="block px-2.5 pb-2.5 pt-4 w-full text-base text-gray-900 tracking-wide bg-white rounded-lg border border-gray-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                    placeholder=" "
                    v-model="registrationdetails.password"
                />
                <div class="absolute right-4">
                    <Transition mode="out-in">
                        <div
                            @click="showpasswords.password = !showpasswords.password"
                            v-if="showpasswords.password"
                            class="w-5 h-5 flex items-center justify-center text-neutral-500 cursor-pointer"
                        >
                            <IconsEye />
                        </div>
                        <div
                            @click="showpasswords.password = !showpasswords.password"
                            v-else
                            class="w-5 h-5 flex items-center justify-center text-neutral-500 cursor-pointer"
                        >
                            <IconsEyeSlash />
                        </div>
                    </Transition>
                </div>
                <label
                    for="pass"
                    class="absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
                    >Password</label
                >
            </div>
            <div class="relative w-[88%] sm:w-[70%] md:w-[60%] lg:w-[40%] flex items-center flex-col gap-y-1">
                <div class="w-full relative flex items-center">
                    <input
                        :type="showpasswords.confirmpassword ? 'password' : 'text'"
                        id="cpass"
                        class="block px-2.5 pb-2.5 pt-4 w-full text-base text-gray-900 tracking-wide bg-white rounded-lg border border-gray-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        placeholder=" "
                        v-model="registrationdetails.confirm_password"
                    />
                    <div class="absolute right-4">
                        <Transition mode="out-in">
                            <div
                                @click="showpasswords.confirmpassword = !showpasswords.confirmpassword"
                                v-if="showpasswords.confirmpassword"
                                class="w-5 h-5 flex items-center justify-center text-neutral-500 cursor-pointer"
                            >
                                <IconsEye />
                            </div>
                            <div
                                @click="showpasswords.confirmpassword = !showpasswords.confirmpassword"
                                v-else
                                class="w-5 h-5 flex items-center justify-center text-neutral-500 cursor-pointer"
                            >
                                <IconsEyeSlash />
                            </div>
                        </Transition>
                    </div>
                    <label
                        for="cpass"
                        class="absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
                    >
                        Confirm Password
                    </label>
                </div>
                <p v-if="details_validation.confirm_password" class="mt-1 text-sm text-red-600 dark:text-red-500 text-start w-full">
                    <span class="font-medium">Please</span> enter a matching password.
                </p>
            </div>
            <div class="w-[88%] sm:w-[70%] md:w-[60%] lg:w-[40%] flex items-center mt-4">
                <button
                    @click="saveNewChild"
                    class="bg-blue-700 text-gray-50 text-lg font-semibold tracking-wide w-full bg-opacity-75 hover:bg-opacity-100 transition duration-200 py-2.5 rounded-lg"
                >
                    <div v-if="submittingdetails">
                        <svg
                            aria-hidden="true"
                            role="status"
                            class="inline w-4 sm:w-5 h-4 sm:h-5 text-white animate-spin"
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
                    </div>
                    <span v-else> Sign up </span>
                </button>
            </div>
            <div class="w-[88%] sm:w-[70%] md:w-[60%] lg:w-[40%] flex flex-col gap-y-3 mt-2 sm:mt-3">
                <div class="or-bar w-full flex flex-row items-center justify-between">
                    <span class="h-[1px] w-[38%] sm:w-[34%] bg-neutral-300"></span>
                    <span class="text-neutral-500 text-base tracking-wide">OR</span>
                    <span class="h-[1px] w-[38%] sm:w-[34%] bg-neutral-300"></span>
                </div>
                <div class="flex items-center justify-center flex-row gap-x-1">
                    <small class="text-sm sm:text-base text-neutral-600">Already have account?</small>
                    <span @click="useRouter().push('/users')" class="text-sm sm:text-base text-blue-700 hover:underline cursor-pointer">
                        Log In
                    </span>
                </div>
            </div>
        </div>
    </main>
</template>
