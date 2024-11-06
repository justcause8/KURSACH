<script setup>
import { onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import useUserStore from './stores/userStore';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const { isAuthenticated, username, userId } = storeToRefs(userStore);

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

async function logout() {
  const csrfToken = Cookies.get('csrftoken');
  try {
    const response = await axios.post('/api/user/logout/', {}, {
      headers: {
        'X-CSRFToken': csrfToken
      }
    });
    if (response.data.success) {
      userStore.resetUser();
      window.location.reload();
    } 
    else {
      console.error('Ошибка выхода, попробуйте еще раз.');
    }
  } catch (error) {
    console.error('Ошибка выхода:', error);
  }
}
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Продажа авто</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/dealer-centers">Dealer-centers</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/dealers">Dealers</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/cars">Cars</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/sales">Sales</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/customers">Customers</router-link>
            </li>
          </ul>

          <ul class="navbar-nav ms-auto">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                aria-expanded="false">
                {{ username }}
              </a>
              <ul class="dropdown-menu">
                <li class="nav-item">
                  <router-link class="nav-link; dropdown-item" to="/login">Войти</router-link>
                </li>
                <li class="nav-item">
                  <a class="dropdown-item" @click="logout">Выход</a>
                </li>
                <li><a class="dropdown-item" href="/admin">Админка</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  <div class="container">
    <router-view />
  </div>
</template>
