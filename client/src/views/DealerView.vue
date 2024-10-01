<script setup>
import { compile, computed, onMounted, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';

const dealers = ref({});
const dealersToAdd = ref({});
const dealersToEdit = ref({});

async function fetchDealers() {
    const r = await axios.get("/api/dealers/")
    dealers.value = r.data;
}

async function onDealersAdd() {
    await axios.post("/api/dealers/", {
        ...dealersToAdd.value,
    });
    await fetchDealers();
}

async function onDealersEditClick(dealer) {
    dealerToEdit.value = {
        ...dealer,
    };
}

async function onDealersUpdateClick() {
    await axios.put(`/api/dealers/${dealersToEdit.value.id}/`, {
        ...dealersToEdit.value
    });
    await fetchDealers();
}

async function onRemoveClick(dealer) {
    await axios.delete(`/api/dealers/${dealer.id}/`)
    await fetchDealers();
}

onBeforeMount(async () => {
    await fetchDealers();
})

</script>
<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent.stop="onDealersAdd">
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="dealersToAdd.name" required>
                            <label for="floatingInput">Location</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="dealersToAdd.headquarters_location"
                                required>
                            <label for="floatingInput">Contact</label>
                        </div>
                    </div>
                    <div class="col">
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-primary">Добавить</button>
                    </div>
                </div>
            </form>
            <div>
                <div v-for='item in dealers' class="dealers-item">
                    <div>{{ item.name }}</div>
                    <div>{{ item.headquarters_location }}</div>
                    <button class="btn btn-success" @click="onDealersEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editDealerCenterModal">
                        <i class="bi bi-pencil-square"></i>
                    </button>
                    <button class="btn btn-danger" @click="onRemoveClick(item)">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            </div>
        </div>
        <!-- Modal -->
        <div class="modal fade" id="editDealerCenterModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Редактировать</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-auto">
                                <div class="form-floating">
                                    <input type="text" class="form-control"
                                        v-model="dealercenterToEdit.headquarters_location">
                                    <label for="floatingInput">Location</label>
                                </div>
                            </div>
                            <div class="col-auto">
                                <div class="form-floating">
                                    <input type="text" class="form-control" v-model="dealercenterToEdit.contact">
                                    <label for="floatingInput">Contact</label>
                                </div>
                            </div>
                            <div class="col-auto">
                                <div class="form-floating">
                                    <input type="text" class="form-control" v-model="dealercenterToEdit.manager">
                                    <label for="floatingInput">Manager</label>
                                </div>
                            </div>
                            <div class="col-auto">
                                <div class="form-floating">
                                    <select class="form-select" v-model="dealercenterToEdit.dealer_FK_id">
                                        <option :value="d.id" v-for="d in dealers">{{ d.name }}</option>
                                    </select>
                                    <label for="floatingInput">Dealer</label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                            @click="onDealersUpdateClick">Сохранить</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.dealers-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    box-shadow: 0 0 4px silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr auto;
    align-content: center;
    align-items: center;
    gap: 16px;
}
</style>