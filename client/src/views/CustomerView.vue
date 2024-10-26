<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import { Modal } from 'bootstrap'

const cars = ref([]);
const customers = ref([]);
const customersToAdd = ref({});
const customersToEdit = ref({});
const confirmDeleteModalRef = ref();
const customerToDelete = ref(null);
const stats = ref({});

function onRemoveClick(customer) {
    customerToDelete.value = customer;
    const confirmModal = new Modal(confirmDeleteModalRef.value);
    confirmModal.show();
}

async function onConfirmDelete() {
    if (customerToDelete.value) {
        await axios.delete(`/api/customers/${customerToDelete.value.id}/`);
        await fetchCustomers();
    }
}

async function fetchCustomers() {
    const r = await axios.get("/api/customers/");
    customers.value = r.data;
}

async function fetchCars() {
    const r = await axios.get("/api/cars/");
    cars.value = r.data;
}

async function onCustomersAdd() {
    await axios.post("/api/customers/", { ...customersToAdd.value });
    await fetchCustomers();
}

async function onCustomersEditClick(customer) {
    customersToEdit.value = {
        ...customer,
        car_FK_id: customer.car_FK.id,
    };
}

async function onCustomersUpdateClick() {
    await axios.put(`/api/customers/${customersToEdit.value.id}/`, {
        ...customersToEdit.value
    });
    await fetchCustomers();
}

async function fetchStats() {
    const r = await axios.get("/api/customers/stats/");
    stats.value = r.data;
}

onBeforeMount(async () => {
    await fetchCars();
    await fetchCustomers();
    await fetchStats();
});
</script>

<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent="onCustomersAdd">
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <select class="form-select" v-model="customersToAdd.car_FK_id" required>
                                <option :value="c.id" v-for="c in cars" :key="c.id">{{ c.car_model }}</option>
                            </select>
                            <label for="floatingInput">Car Model</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="customersToAdd.name" required>
                            <label for="floatingInput">Name</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="customersToAdd.contact_info" required>
                            <label for="floatingInput">Contact info</label>
                        </div>
                    </div>
                    <div class="col-auto d-flex align-self-center">
                        <button class="btn btn-primary">Добавить</button>
                    </div>
                    <div class="col-auto d-flex align-self-center">
                        <button class="btn btn-success" @click="fetchStats()" data-bs-toggle="modal"
                            data-bs-target="#statsModal">Статистика</button>
                    </div>
                </div>
            </form>
            <div>
                <div v-for="customer in customers" :key="customer.id" class="customers-item">
                    <div>{{ customer.car_FK.car_model }}</div>
                    <div>{{ customer.name }}</div>
                    <div>{{ customer.contact_info }}</div>
                    <button class="btn btn-success" @click="onCustomersEditClick(customer)" data-bs-toggle="modal"
                        data-bs-target="#editCustomersModal">
                        <i class="bi bi-pencil-square"></i>
                    </button>
                    <button class="btn btn-danger" @click="onRemoveClick(customer)">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="editCustomersModal" tabindex="-1">
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
                                <select class="form-select" v-model="customersToEdit.car_FK_id">
                                    <option :value="c.id" v-for="c in cars" :key="c.id">{{ c.car_model }}</option>
                                </select>
                                <label for="floatingInput">Car model</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="customersToEdit.name">
                                <label for="floatingInput">Name</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="customersToEdit.contact_info">
                                <label for="floatingInput">Contact info</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                        @click="onCustomersUpdateClick">Сохранить</button>
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
                    Вы уверены, что хотите удалить "{{ customerToDelete?.name }}"?
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
                    <h5 class="modal-title">Статистика Покупателей</h5>
                </div>
                <div class="modal-body">
                    <p>Количество Покупателей: {{ stats.count }}</p>
                    <p>Максимальный ID Покупателя: {{ stats.max }}</p>
                    <p>Минимальный ID Покупателя: {{ stats.min }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.customers-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    box-shadow: 0 0 4px silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr auto auto;
    align-content: center;
    align-items: center;
    gap: 16px;
}
</style>