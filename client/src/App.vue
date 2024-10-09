<script setup>
import { onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Navbar</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-cintent-between" id="navbarNav">
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

          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                aria-expanded="false">
                Пользователь
              </a>
              <ul class="dropdown-menu">
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

<style></style>