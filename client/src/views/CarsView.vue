<script setup>
import { compile, computed, onMounted, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';

const cars = ref([]);
const dealer_centers = ref([]);
const dealers = ref([]);
const carsToAdd = ref({
    dealer_FK_id: null,
    dealer_center_FK_id: null,
    car_model: '',
    year: '',
    price: ''
});
const carsToEdit = ref({});

async function fetchCars() {
    const r = await axios.get("/api/cars/");
    cars.value = r.data;
}

async function fetchDealerCenters() {
    const r = await axios.get("/api/dealer-centers/");
    dealer_centers.value = r.data;
}

async function fetchDealers() {
    const r = await axios.get("/api/dealers/");
    dealers.value = r.data;
}

async function onCarsAdd() {
    await axios.post("/api/cars/", { ...carsToAdd.value });
    await fetchCars();
}

async function onCarsEditClick(car) {
    carsToEdit.value = {
        ...car,
        dealer_FK_id: car.dealer_FK.id,
        dealer_center_FK_id: car.dealer_center_FK.id,
    };
}

async function onCarsUpdateClick() {
    await axios.put(`/api/cars/${carsToEdit.value.id}/`, {
        ...carsToEdit.value
    });
    await fetchCars();
}

async function onRemoveClick(car) {
    await axios.delete(`/api/cars/${car.id}/`);
    await fetchCars();
}

// Вычисляемое свойство для фильтрации дилерских центров по выбранному дилеру
const filteredDealerCenters = computed(() => {
    if (!carsToAdd.value.dealer_FK_id) return [];
    return dealer_centers.value.filter(center => center.dealer_FK.id === carsToAdd.value.dealer_FK_id);
});

// Вычисляемое свойство для фильтрации дилерских центров для редактирования
const filteredDealerCentersForEdit = computed(() => {
    if (!carsToEdit.value.dealer_FK_id) return [];
    return dealer_centers.value.filter(center => center.dealer_FK.id === carsToEdit.value.dealer_FK_id);
});


onBeforeMount(async () => {
    await fetchCars();
    await fetchDealers();
    await fetchDealerCenters();
});
</script>

<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent.stop="onCarsAdd">
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <select class="form-select" v-model="carsToAdd.dealer_FK_id" required>
                                <option :value="d.id" v-for="d in dealers" :key="d.id">{{ d.name }}</option>
                            </select>
                            <label for="floatingInput">Dealer</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="carsToAdd.car_model" required>
                            <label for="floatingInput">Model</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="carsToAdd.year" required>
                            <label for="floatingInput">Year</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="carsToAdd.price" required>
                            <label for="floatingInput">Price</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <select class="form-select" v-model="carsToAdd.dealer_center_FK_id" required>
                                <option :value="d.id" v-for="d in filteredDealerCenters" :key="d.id">
                                    {{ d.headquarters_location }}
                                </option>
                            </select>
                            <label for="floatingInput">Dealer Center</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-primary">Добавить</button>
                    </div>
                </div>
            </form>
            <div>
                <div v-for='item in cars' class="cars-item">
                    <div>{{ item.dealer_FK.name }}</div>
                    <div>{{ item.car_model }}</div>
                    <div>{{ item.year }}</div>
                    <div>{{ item.price }}</div>
                    <div>{{ item.dealer_center_FK.headquarters_location }}</div>
                    <button class="btn btn-success" @click="onCarsEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editCarsModal">
                        <i class="bi bi-pencil-square"></i>
                    </button>
                    <button class="btn btn-danger" @click="onRemoveClick(item)">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal для редактирования -->
    <div class="modal fade" id="editCarsModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Редактировать</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-auto">
                            <div class="form-floating">
                                <select class="form-select" v-model="carsToEdit.dealer_FK_id">
                                    <option :value="d.id" v-for="d in dealers">{{ d.name }}</option>
                                </select>
                                <label for="floatingInput">Dealer</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="carsToEdit.car_model">
                                <label for="floatingInput">Model</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="carsToEdit.year">
                                <label for="floatingInput">Year</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="carsToEdit.price">
                                <label for="floatingInput">Price</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <select class="form-select" v-model="carsToEdit.dealer_center_FK_id">
                                    <option :value="d.id" v-for="d in filteredDealerCentersForEdit">{{ d.headquarters_location }}</option>
                                </select>
                                <label for="floatingInput">Dealer center</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                        @click="onCarsUpdateClick">Сохранить</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.cars-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    box-shadow: 0 0 4px silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr auto auto auto auto;
    align-content: center;
    align-items: center;
    gap: 16px;
}
</style>