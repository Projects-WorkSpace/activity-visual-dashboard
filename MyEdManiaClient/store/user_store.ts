import { defineStore } from 'pinia';
import { UserDetails } from '~~/Types/UserDetails';

export const useAuthStore = defineStore('auth', () => {
    const authDetails = ref<UserDetails>();

    const updateAuthDetails = (details: UserDetails): void => {
        authDetails.value = details;
    };

    return { authDetails, updateAuthDetails };
});
