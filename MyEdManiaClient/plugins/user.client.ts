import { useAuthStore } from '~~/store/user_store';
export default defineNuxtPlugin((NuxtApp) => {
    const local_user: string | null = localStorage.getItem('edmania_user');

    const useAuth = useAuthStore();
    if (local_user !== null) {
        useAuth.updateAuthDetails(JSON.parse(local_user));
    }
});
