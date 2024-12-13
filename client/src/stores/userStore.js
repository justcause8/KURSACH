import { onBeforeMount } from "vue";
import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

const useUserStore = defineStore("UserStore", () => {
    const isAuthenticated = ref(false);
    const username = ref("");
    const userId = ref();
    const isSuperuser = ref(false);
    const users = ref([]);

    async function fetchUsers() {
        const r = await axios.get("/api/user/list-users/");
        users.value = r.data;
    }
    
    async function fetchUser() {
        const response = await axios.get("/api/user/info/");
        isAuthenticated.value = response.data.is_authenticated;
        username.value = response.data.username;
        userId.value = response.data.user_id;
        isSuperuser.value = response.data.is_superuser || false;

        if (isSuperuser.value) {
            await fetchUsers();
        }
    }

    function resetUser() {
        isAuthenticated.value = false;
        username.value = "";
        userId.value = null;
    }

    onBeforeMount(() => {
        fetchUser();
    })

    return {
        isAuthenticated,
        username,
        userId,
        isSuperuser,
        users,
        fetchUser,
        fetchUsers,
        resetUser
    };
})

export default useUserStore;