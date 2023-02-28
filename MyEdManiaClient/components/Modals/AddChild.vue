<script lang="ts" setup>
import { useAuthStore } from '~~/store/user_store';
import { ChildModel } from '~~/Types/General';

const emits = defineEmits<{
    (e: 'closeModal'): void;
    (e: 'updateChildrenList', child: ChildModel): void;
}>();

const config = useRuntimeConfig();
const useAuth = useAuthStore();
const submittingnewchild = ref<boolean>(false);

const childdetails = ref<{
    name: string;
    dob: Date | undefined;
}>({ name: '', dob: undefined });
const childdetailsvalidations = ref<{
    name: boolean;
    dob: boolean;
}>({ name: false, dob: false });

const submitChildDetails = (): void => {
    childdetailsvalidations.value.name = false;
    childdetailsvalidations.value.dob = false;
    console.log(childdetails.value.dob);
    if (childdetails.value.name === '') {
        childdetailsvalidations.value.name = true;
        return;
    } else if (childdetails.value.dob === undefined) {
        childdetailsvalidations.value.dob = true;
        return;
    } else {
        submittingnewchild.value = true;
        fetchPostChild();
        setTimeout(() => {
            submittingnewchild.value = false;
        }, 500);
    }
};

const fetchPostChild = async (): Promise<void> => {
    const { data: child, error } = await useFetch<string, ChildModel>(config.public.apiBase + '/api/mychild', {
        method: 'Post',
        headers: {
            Authorization: useAuth.authDetails?.Authorization || '',
        },
        body: {
            name: childdetails.value.name,
            dateOfBirth: childdetails.value.dob,
        },
    });
    if (error.value) {
        console.log(error.value);
        return;
    } else {
        emits('updateChildrenList', child.value as unknown as ChildModel);
        emits('closeModal');
    }
};
</script>
<template>
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
            <div class="px-6 py-3 border-b rounded-t dark:border-gray-600">
                <h3 class="text-base font-semibold text-gray-900 lg:text-xl dark:text-white">Add another child</h3>
            </div>
        </div>
        <div class="w-full flex flex-col gap-y-3.5 px-6 py-3">
            <div>
                <label for="full_name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Full name</label>
                <input
                    type="text"
                    id="full_name"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 outline-none"
                    placeholder="John Doe"
                    v-model="childdetails.name"
                />
                <p v-if="childdetailsvalidations.name" class="mt-1 text-sm text-red-600 dark:text-red-500">
                    <span class="font-medium">Please</span> enter a valid name.
                </p>
            </div>
            <div class="">
                <label for="dob" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Date of birth</label>
                <div class="relative z-10">
                    <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
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
                    </div>
                    <input
                        type="date"
                        v-model="childdetails.dob"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5 focus:outline-none"
                        placeholder="Select date"
                    />
                    <p v-if="childdetailsvalidations.dob" class="mt-1 text-sm text-red-600 dark:text-red-500">
                        <span class="font-medium">Please</span> enter a valid date.
                    </p>
                </div>
            </div>
        </div>
        <div class="w-full flex flex-row gap-x-2 items-center py-3.5 px-6">
            <button
                @click="submitChildDetails"
                type="button"
                class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-2 focus:ring-blue-300 font-medium rounded-lg text-base px-5 py-2.5"
            >
                <Transition mode="out-in">
                    <div v-if="submittingnewchild">
                        <svg
                            aria-hidden="true"
                            role="status"
                            class="inline w-4 h-4 mr-3 text-white animate-spin"
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
                    <span v-else> Save </span>
                </Transition>
            </button>
        </div>
    </div>
</template>
