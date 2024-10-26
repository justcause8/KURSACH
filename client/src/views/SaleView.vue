<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';
import { Modal } from 'bootstrap'

const sales = ref([]);
const cars = ref([]);
const customers = ref([]);
const salesToAdd = ref({});
const salesToEdit = ref({});
const confirmDeleteModalRef = ref();
const saleToDelete = ref(null);
const stats = ref({});

function onRemoveClick(sale) {
    saleToDelete.value = sale;
    const confirmModal = new Modal(confirmDeleteModalRef.value);
    confirmModal.show();
}

async function onConfirmDelete() {
    if (saleToDelete.value) {
        await axios.delete(`/api/sales/${saleToDelete.value.id}/`);
        await fetchSales();
    }
}

async function fetchSales() {
    const r = await axios.get("/api/sales/");
    sales.value = r.data;
}

async function fetchCustomers() {
    const r = await axios.get("/api/customers/");
    customers.value = r.data;
}

async function fetchCars() {
    const r = await axios.get("/api/cars/");
    cars.value = r.data;
}

async function onSalesAdd() {
    await axios.post("/api/sales/", { ...salesToAdd.value });
    await fetchSales();
}

async function onSalesEditClick(sale) {
    salesToEdit.value = {
        ...sale,
        customer_FK_id: sale.customer_FK.id,
        car_FK_id: sale.car_FK.id,
    };
}

async function onSalesUpdateClick() {
    await axios.put(`/api/sales/${salesToEdit.value.id}/`, {
        ...salesToEdit.value
    });
    await fetchSales();
}

async function fetchStats() {
    const r = await axios.get("/api/sales/stats/");
    stats.value = r.data;
}

onBeforeMount(async () => {
    await fetchCars();
    await fetchSales();
    await fetchCustomers();
    await fetchStats();
});

</script>
<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent.stop="onSalesAdd">
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <select class="form-select" v-model="salesToAdd.car_FK_id" required>
                                <option :value="c.id" v-for="c in cars" :key="c.id">{{ c.car_model }}</option>
                            </select>
                            <label for="floatingInput">Car Model</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <select class="form-select" v-model="salesToAdd.customer_FK_id" required>
                                <option :value="c.id" v-for="c in customers" :key="c.id">
                                    {{ c.name }}
                                </option>
                            </select>
                            <label for="floatingInput">Customer</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="date" class="form-control" v-model="salesToAdd.sale_data" required>
                            <label for="floatingInput">Sale Date</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="salesToAdd.sale_price" required>
                            <label for="floatingInput">Sale Price</label>
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
                <div v-for="item in sales" :key="item.id" class="sales-item">
                    <div>{{ item.car_FK.car_model }}</div>
                    <div>{{ item.customer_FK.name }}</div>
                    <div>{{ item.sale_data }}</div>
                    <div>{{ item.sale_price }}</div>
                    <button class="btn btn-success" @click="onSalesEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editSalesModal">
                        <i class="bi bi-pencil-square"></i>
                    </button>
                    <button class="btn btn-danger" @click="onRemoveClick(item)">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="editSalesModal" tabindex="-1">
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
                                <select class="form-select" v-model="salesToEdit.car_FK_id">
                                    <option :value="c.id" v-for="c in cars" :key="c.id">{{ c.car_model }}</option>
                                </select>
                                <label for="floatingInput">Car</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <select class="form-select" v-model="salesToEdit.customer_FK_id">
                                    <option :value="c.id" v-for="c in customers">{{ c.name }}</option>
                                </select>
                                <label for="floatingInput">Customer</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <input type="date" class="form-control" v-model="salesToEdit.sale_data">
                                <label for="floatingInput">Sale Date</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="salesToEdit.sale_price">
                                <label for="floatingInput">Sale Price</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                        @click="onSalesUpdateClick">Сохранить</button>
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
                    Вы уверены, что хотите удалить продажу от "{{ saleToDelete?.sale_data }}"?
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
                    <h5 class="modal-title">Статистика Продаж</h5>
                </div>
                <div class="modal-body">
                    <p>Количество Продаж: {{ stats.count }}</p>
                    <p>Максимальный ID Продажи: {{ stats.max }}</p>
                    <p>Минимальный ID Продажи: {{ stats.min }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.sales-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    box-shadow: 0 0 4px silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr auto auto;
    align-content: center;
    align-items: center;
    gap: 16px;
}
</style>
