<script setup>
import { ref, computed, onBeforeMount } from 'vue';
import axios from 'axios';
import { Modal } from 'bootstrap'

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
const filters = ref({
    dealer_FK: "",
    dealer_center_FK: "",
    car_model: "",
    year: "",
    price: ""
});

const carsToEdit = ref({});
const carPictureRef = ref('');
const carPictureRefEdit = ref('');
const carsAddImageUrl = ref('');
const carsEditImageUrl = ref('');
const selectedImageUrl = ref(null);
const imageModalRef = ref();
const confirmDeleteModalRef = ref();
const carToDelete = ref(null);
const stats = ref({});

function onRemoveClick(car) {
    carToDelete.value = car;
    const confirmModal = new Modal(confirmDeleteModalRef.value);
    confirmModal.show();
}

async function onConfirmDelete() {
    if (carToDelete.value) {
        await axios.delete(`/api/cars/${carToDelete.value.id}/`);
        await fetchCars();
    }
}

function onImageClick(imageUrl) {
    selectedImageUrl.value = imageUrl;
    const imageModal = new Modal(imageModalRef.value);
    imageModal.show();
}

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
    const formData = new FormData();

    formData.append('car_model', carsToAdd.value.car_model);
    formData.append('year', carsToAdd.value.year);
    formData.append('price', carsToAdd.value.price);
    formData.append('dealer_FK_id', carsToAdd.value.dealer_FK_id);
    formData.append('dealer_center_FK_id', carsToAdd.value.dealer_center_FK_id);

    if (carPictureRef.value && carPictureRef.value.files.length > 0) {
        formData.append('picture', carPictureRef.value.files[0]);
    }

    await axios.post("/api/cars/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchCars();
}

async function onCarsEditClick(car) {
    carsToEdit.value = {
        ...car,
        dealer_FK_id: car.dealer_FK.id,
        dealer_center_FK_id: car.dealer_center_FK.id,
    };
    carsEditImageUrl.value = car.picture;
}

async function onCarsUpdateClick() {
    const formData = new FormData();

    if (carPictureRefEdit.value && carPictureRefEdit.value.files.length > 0) {
        formData.append('picture', carPictureRefEdit.value.files[0]);
    }

    formData.set('car_model', carsToEdit.value.car_model);
    formData.set('year', carsToEdit.value.year);
    formData.set('price', carsToEdit.value.price);
    formData.set('dealer_FK_id', carsToEdit.value.dealer_FK_id);
    formData.set('dealer_center_FK_id', carsToEdit.value.dealer_center_FK_id);

    await axios.put(`/api/cars/${carsToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchCars();
}

async function carsAddPictureChange() {
    if (carPictureRef.value && carPictureRef.value.files.length > 0) {
        carsAddImageUrl.value = URL.createObjectURL(carPictureRef.value.files[0]);
    }
}

async function carsEditPictureChange() {
    if (carPictureRefEdit.value && carPictureRefEdit.value.files.length > 0) {
        carsEditImageUrl.value = URL.createObjectURL(carPictureRefEdit.value.files[0]);
    }
}

const filteredDealerCenters = computed(() => {
    if (!carsToAdd.value.dealer_FK_id) return [];
    return dealer_centers.value.filter(center => center.dealer_FK.id === carsToAdd.value.dealer_FK_id);
});

const filteredDealerCentersForEdit = computed(() => {
    if (!carsToEdit.value.dealer_FK_id) return [];
    return dealer_centers.value.filter(center => center.dealer_FK.id === carsToEdit.value.dealer_FK_id);
});

async function fetchStats() {
    const r = await axios.get("/api/cars/stats/");
    stats.value = r.data;
}

// Фильтровать автомобили по введённым значениям
const filteredCars = computed(() => {
    return cars.value.filter(car => {
        const dealerMatch = !filters.value.dealer_FK || car.dealer_FK.id.toString().includes(filters.value.dealer_FK);
        const modelMatch = !filters.value.car_model || car.car_model.toLowerCase().includes(filters.value.car_model.toLowerCase());
        const yearMatch = !filters.value.year || car.year.toString().includes(filters.value.year);
        const priceMatch = !filters.value.price || car.price.toString().includes(filters.value.price);
        const centerMatch = !filters.value.dealer_center_FK || car.dealer_center_FK.id.toString().includes(filters.value.dealer_center_FK);

        return dealerMatch && modelMatch && yearMatch && priceMatch && centerMatch;
    });
});

function resetFilters() {
    filters.value = {
        dealer_FK: "",
        dealer_center_FK: "",
        car_model: "",
        year: "",
        price: ""
    };
}

onBeforeMount(async () => {
    await fetchCars();
    await fetchDealers();
    await fetchDealerCenters();
    await fetchStats();
});

async function exportToExcel() {
    const response = await axios.get("/api/cars/export-excel/", { responseType: "blob" });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "cars.xlsx");
    document.body.appendChild(link);
    link.click();
}

async function exportToWord() {
    const response = await axios.get("/api/cars/export-word/", { responseType: "blob" });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "cars.docx");
    document.body.appendChild(link);
    link.click();
}
</script>

<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent="onCarsAdd">
                <h4>Ввод данных</h4>
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
                                <option :value="d.id" v-for="d in filteredDealerCenters">{{ d.headquarters_location }}
                                </option>
                            </select>
                            <label for="floatingInput">Dealer Center</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <input class="form-control" type="file" ref="carPictureRef" @change="carsAddPictureChange">
                    </div>
                    <div class="col-auto">
                        <img v-if="carsAddImageUrl" :src="carsAddImageUrl" style="max-height: 60px;" alt="">
                    </div>
                    <div class="col-auto d-flex align-self-center">
                        <button class="btn btn-primary">Добавить</button>
                    </div>
                </div>
            </form>
            <div class="col-auto d-flex justify-content-end mt-2">
                <button class="btn btn-success me-2" @click="exportToExcel">
                    Сохранить в Excel
                </button>

                <button class="btn btn-success me-2" @click="exportToWord">
                    Сохранить в Word
                </button>

                <button class="btn btn-success" @click="fetchStats()" data-bs-toggle="modal"
                    data-bs-target="#statsModal">
                    Статистика
                </button>
            </div>

            <h4>Фильтрация</h4>
            <div class="row mb-3 mt-3">
                <div class="col">
                    <select class="form-select" v-model="filters.dealer_FK">
                        <option value="">Dealers</option>
                        <option :value="d.id" v-for="d in dealers" :key="d.id">{{ d.name }}</option>
                    </select>
                </div>
                <div class="col">
                    <input type="text" class="form-control" placeholder="Model" v-model="filters.car_model">
                </div>
                <div class="col">
                    <input type="text" class="form-control" placeholder="Year" v-model="filters.year">
                </div>
                <div class="col">
                    <input type="text" class="form-control" placeholder="Price" v-model="filters.price">
                </div>
                <div class="col">
                    <select class="form-select" v-model="filters.dealer_center_FK">
                        <option value="">Dealer centers</option>
                        <option v-for="c in dealer_centers" :key="c.id" :value="c.id">
                            {{ c.headquarters_location }}
                        </option>
                    </select>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary" @click="resetFilters">Сбросить</button>
                </div>
            </div>

            <div v-if="filteredCars.length > 0">
                <div v-for='item in filteredCars' class="cars-item">
                    <div>{{ item.dealer_FK.name }}</div>
                    <div>{{ item.car_model }}</div>
                    <div>{{ item.year }}</div>
                    <div>{{ item.price }}</div>
                    <div>{{ item.dealer_center_FK.headquarters_location }}</div>
                    <div v-if="item.picture">
                        <img :src="item.picture" style="max-height: 60px; cursor: pointer;" alt="Car image"
                            @click="onImageClick(item.picture)">
                    </div>
                    <div class="d-flex justify-content-end">
                        <button class="btn btn-success  me-1" @click="onCarsEditClick(item)" data-bs-toggle="modal"
                            data-bs-target="#editCarsModal">
                            <i class="bi bi-pencil-square"></i>
                        </button>
                        <button class="btn btn-danger" @click="onRemoveClick(item)">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div v-else class="text-center mt-4">
                <img src="D:\ПОЛИТЕХ\3 курс\web-программирование\KURSACH\media\other\huh-pulp.gif" alt="Huh Pulp GIF"
                    style="max-width: 100px; height: auto;">
            </div>
        </div>
    </div>

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
                                <select class="form-select" v-model="carsToEdit.dealer_FK_id" required>
                                    <option :value="d.id" v-for="d in dealers" :key="d.id">{{ d.name }}</option>
                                </select>
                                <label for="floatingInput">Dealer</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="carsToEdit.car_model" required>
                                <label for="floatingInput">Model</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="carsToEdit.year" required>
                                <label for="floatingInput">Year</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="carsToEdit.price" required>
                                <label for="floatingInput">Price</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <select class="form-select" v-model="carsToEdit.dealer_centers_FK_id" required>
                                    <option :value="d.id" v-for="d in filteredDealerCentersForEdit" :key="d.id">{{
                                        d.headquarters_location }}</option>
                                </select>
                                <label for="floatingInput">Dealer center</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <input class="form-control" type="file" ref="carPictureRefEdit"
                                @change="carsEditPictureChange">
                        </div>
                        <div class="col-auto">
                            <img v-if="carsEditImageUrl" :src="carsEditImageUrl" style="max-height: 60px;" alt="">
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                        @click="onCarsUpdateClick">Обновить</button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" ref="imageModalRef" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-body">
                    <img :src="selectedImageUrl" alt="Car Image" class="img-fluid">
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" ref="confirmDeleteModalRef" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Подтверждение удаления</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Вы уверены, что хотите удалить "{{ carToDelete?.car_model }}"?
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                    <button type="button" class="btn btn-danger" @click="onConfirmDelete"
                        data-bs-dismiss="modal">Удалить</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Модальное окно для статистики -->
    <div class="modal fade" id="statsModal" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Статистика Автомобилей</h5>
                </div>
                <div class="modal-body">
                    <p>Количество Автомобилей: {{ stats.count }}</p>
                    <p>Максимальный ID Автомобиля: {{ stats.max }}</p>
                    <p>Минимальный ID Автомобиля: {{ stats.min }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
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
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr auto auto;
    align-content: center;
    align-items: center;
    gap: 16px;
}
</style>