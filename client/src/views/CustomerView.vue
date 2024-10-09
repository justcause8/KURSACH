<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';

const cars = ref([]);
const customers = ref([]);
const customersToAdd = ref({});
const customersToEdit = ref({});

// Получение списка клиентов
async function fetchCustomers() {
    const r = await axios.get("/api/customers/");
    customers.value = r.data;
}

// Получение списка автомобилей
async function fetchCars() {
    const r = await axios.get("/api/cars/");
    cars.value = r.data;
}

// Добавление клиента
async function onCustomersAdd() {
    await axios.post("/api/customers/", { ...customersToAdd.value });
    await fetchCustomers();
}

// Редактирование клиента
async function onCustomersEditClick(customer) {
    customersToEdit.value = {
        ...customer,
        car_FK_id: customer.car_FK.id, // Исправлено на использование правильного объекта
    };
}

// Обновление данных клиента
async function onCustomersUpdateClick() {
    await axios.put(`/api/customers/${customersToEdit.value.id}/`, {
        ...customersToEdit.value
    });
    await fetchCustomers();
}

// Удаление клиента
async function onRemoveClick(customer) {
    await axios.delete(`/api/customers/${customer.id}/`);
    await fetchCustomers();
}

// Инициализация данных при загрузке компонента
onBeforeMount(async () => {
    await fetchCars();
    await fetchCustomers();
});
</script>

<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent="onCustomersAdd">
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <!-- Выбор модели автомобиля -->
                            <select class="form-select" v-model="customersToAdd.car_FK_id" required>
                                <option :value="c.id" v-for="c in cars" :key="c.id">{{ c.car_model }}</option>
                            </select>
                            <label for="floatingInput">Car Model</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <!-- Имя клиента -->
                            <input type="text" class="form-control" v-model="customersToAdd.name" required>
                            <label for="floatingInput">Name</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <!-- Контактная информация -->
                            <input type="text" class="form-control" v-model="customersToAdd.contact_info" required>
                            <label for="floatingInput">Contact info</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-primary">Добавить</button>
                    </div>
                </div>
            </form>
            <div>
                <!-- Список клиентов -->
                <div v-for="customer in customers" :key="customer.id" class="customers-item">
                    <div>{{ customer.car_FK.car_model }}</div>
                    <div>{{ customer.name }}</div>
                    <div>{{ customer.contact_info }}</div>
                    <!-- Кнопка для редактирования -->
                    <button class="btn btn-success" @click="onCustomersEditClick(customer)" data-bs-toggle="modal"
                        data-bs-target="#editCustomersModal">
                        <i class="bi bi-pencil-square"></i>
                    </button>
                    <!-- Кнопка для удаления -->
                    <button class="btn btn-danger" @click="onRemoveClick(customer)">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Модальное окно для редактирования клиента -->
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
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onCustomersUpdateClick">Сохранить</button>
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