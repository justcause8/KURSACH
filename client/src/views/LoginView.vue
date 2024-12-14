<script setup>
import { storeToRefs } from 'pinia';
import useUserStore from '@/stores/userStore';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import Cookies from 'js-cookie';

const username = ref("");
const pas = ref("");
const router = useRouter();

const userStore = useUserStore();
const { isAuthenticated } = storeToRefs(userStore);

async function login() {
    const csrfToken = Cookies.get('csrftoken');

    try {
        const response = await axios.post("/api/user/login/", {
            user: username.value,
            password: pas.value
        }, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        if (response.status === 200) {
            await userStore.fetchUser();
            router.push("/");
        } else {
        }
    } catch (error) {
        console.error("Ошибка входа:", error);
    }
}
</script>

<template>
    <section class="vh-75 gradient-custom">
        <div class="container py-5 h-100">
            <div class="row d-flex justify-content-center align-items-center h-100">
                <div class="col-10 col-md-6 col-lg-5 col-xl-4">
                    <div class="card custom-bg text-white" style="border-radius: 1rem;">
                        <div class="card-body p-4 text-center">
                            <div class="mb-md-4 mt-md-2 pb-3">
                                <h2 class="fw-bold mb-2 text-uppercase">Login</h2>
                                <div class="form-outline form-white mb-3">
                                    <input v-model="username" id="Login" class="form-control form-control-sm" />
                                    <label class="form-label" for="Login">Username</label>
                                </div>
                                <div class="form-outline form-white mb-3">
                                    <input type="password" v-model="pas" id="typePasswordX"
                                        class="form-control form-control-sm" />
                                    <label class="form-label" for="typePasswordX">Password</label>
                                </div>
                                <button @click="login" class="btn btn-outline-light btn-sm px-4"
                                    type="submit">Login</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<style>
.vh-75 {
    height: 75vh;
}

.custom-bg {
    background-color: #333366;
    border-radius: 1rem;
    height: 300px;
}

.card-body {
    padding: 1.5rem;
}

.btn-outline-light {
    color: #f8f9fa;
    border-color: #f8f9fa;
}

.btn-outline-light:hover {
    background-color: #f8f9fa;
    color: #333366;
}
</style>