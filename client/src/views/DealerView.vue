<script setup>
import { ref, computed, onBeforeMount } from 'vue';
import axios from 'axios';
import { Modal } from 'bootstrap'
import { storeToRefs } from 'pinia';
import useUserStore from '../stores/userStore';

const dealersPictureRef = ref('');
const dealersPictureRefEdit = ref('');
const dealersAddImageUrl = ref('');
const dealersEditImageUrl = ref('');
const selectedImageUrl = ref();
const imageModalRef = ref();
const confirmDeleteModalRef = ref();
const dealerToDelete = ref(null);
const dealers = ref([]);
const stats = ref({});
const userStore = useUserStore();
const { isSuperuser, users } = storeToRefs(userStore);

const filters = ref({
    name: "",
    headquarters_location: "",
    user_id: ""
});

const dealersToAdd = ref({
    name: '',
    headquarters_location: '',
});
const dealersToEdit = ref({
    name: '',
    headquarters_location: '',
    picture: '',
});

function onImageClick(imageUrl) {
    selectedImageUrl.value = imageUrl;
    const imageModal = new Modal(imageModalRef.value);
    imageModal.show();
}

function onRemoveClick(dealer) {
    dealerToDelete.value = dealer;
    const confirmModal = new Modal(confirmDeleteModalRef.value);
    confirmModal.show();
}

async function onConfirmDelete() {
    if (dealerToDelete.value) {
        await axios.delete(`/api/dealers/${dealerToDelete.value.id}/`);
        await fetchDealers();
    }
}

async function fetchDealers() {
    const r = await axios.get("/api/dealers/");
    dealers.value = r.data;
}

async function onDealersAdd() {
    const formData = new FormData();

    if (dealersPictureRef.value && dealersPictureRef.value.files.length > 0) {
        formData.append('picture', dealersPictureRef.value.files[0]);
    }

    formData.set('name', dealersToAdd.value.name);
    formData.set('headquarters_location', dealersToAdd.value.headquarters_location);

    await axios.post("/api/dealers/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        }
    });
    await fetchDealers();

}

async function dealersAddPictureChange() {
    if (dealersPictureRef.value && dealersPictureRef.value.files.length > 0) {
        dealersAddImageUrl.value = URL.createObjectURL(dealersPictureRef.value.files[0]);
    }
}

async function dealersEditPictureChange() {
    if (dealersPictureRefEdit.value && dealersPictureRefEdit.value.files.length > 0) {
        dealersEditImageUrl.value = URL.createObjectURL(dealersPictureRefEdit.value.files[0]);
    }
}

async function onDealersEditClick(dealer) {
    dealersToEdit.value = { ...dealer };
    dealersEditImageUrl.value = dealer.picture;
}

async function onDealersUpdateClick() {
    const formData = new FormData();

    if (dealersPictureRefEdit.value && dealersPictureRefEdit.value.files.length > 0) {
        formData.append('picture', dealersPictureRefEdit.value.files[0]);
    }

    formData.set('name', dealersToEdit.value.name);
    formData.set('headquarters_location', dealersToEdit.value.headquarters_location);

    await axios.put(`/api/dealers/${dealersToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchDealers();
}

async function fetchStats() {
    const r = await axios.get("/api/dealers/stats/");
    stats.value = r.data;
}

// Фильтровать дилеров по введённым значениям
const filteredDealers = computed(() => {
    return dealers.value.filter(dealer => {
        const nameMatch = !filters.value.name || dealer.name.trim().toLowerCase().includes(filters.value.name.trim().toLowerCase());
        const locationMatch = !filters.value.headquarters_location || dealer.headquarters_location.trim().toLowerCase().includes(filters.value.headquarters_location.trim().toLowerCase());
        const userMatch = !filters.value.user_id || dealer.user === filters.value.user_id;

        return nameMatch && locationMatch && userMatch;
    });
});

function resetFilters() {
    filters.value = {
        name: "",
        headquarters_location: "",
        user_id: ""
    };
}

onBeforeMount(async () => {
    await userStore.fetchUser();
    if (isSuperuser.value) {
        await userStore.fetchUsers();
    }
    await fetchDealers();
    await fetchStats();
});
</script>

<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent="onDealersAdd">
                <h4>Ввод данных</h4>
                <div class="row align-items-center g-2">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="dealersToAdd.name" required>
                            <label for="floatingInput">Name</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="dealersToAdd.headquarters_location"
                                required>
                            <label for="floatingInput">Location</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <input class="form-control" type="file" ref="dealersPictureRef"
                            @change="dealersAddPictureChange">
                    </div>
                    <div class="col-auto">
                        <img v-if="dealersAddImageUrl" :src="dealersAddImageUrl" style="max-height: 60px;" alt="">
                    </div>
                    <div class="col-auto d-flex align-self-center">
                        <button class="btn btn-primary">Добавить</button>
                    </div>
                </div>
            </form>
            <div class="col-auto d-flex justify-content-end mt-2">
                <button class="btn btn-success" @click="fetchStats()" data-bs-toggle="modal"
                    data-bs-target="#statsModal">Статистика</button>
            </div>

            <h4>Фильтрация</h4>
            <div class="row mb-3 mt-3">
                <div class="col">
                    <input type="text" class="form-control" placeholder="Name" v-model="filters.name">
                </div>
                <div class="col">
                    <input type="text" class="form-control" placeholder="Location"
                        v-model="filters.headquarters_location">
                </div>   
                <div class="col">
                    <select class="form-select" v-model="filters.user_id">
                        <option value="">Users</option>
                        <option v-for="user in users" :key="user.id" :value="user.id">
                            {{ user.username }}
                        </option>
                    </select>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary" @click="resetFilters">Сбросить</button>
                </div>
            </div>

            <div v-if="filteredDealers.length > 0">
                <div v-for="item in filteredDealers" class="dealers-item">
                    <div>{{ item.name }}</div>
                    <div>{{ item.headquarters_location }}</div>
                    <div v-if="item.picture">
                        <img :src="item.picture" style="max-height: 60px; cursor: pointer;" alt="Car image"
                            @click="onImageClick(item.picture)">
                    </div>
                    <div class="d-flex justify-content-end">
                        <button class="btn btn-success me-1" @click="onDealersEditClick(item)" data-bs-toggle="modal"
                            data-bs-target="#editDealersModal">
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

        <div class="modal fade" id="editDealersModal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Редактировать</h5>
                    </div>
                    <div class="modal-body m">
                        <div class="row p-1">
                            <div class="col">
                                <div class="form-floating">
                                    <input type="text" class="form-control" v-model="dealersToEdit.name">
                                    <label for="floatingInput">Name</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <input type="text" class="form-control"
                                        v-model="dealersToEdit.headquarters_location">
                                    <label for="floatingInput">Location</label>
                                </div>
                            </div>
                        </div>
                        <div class="row p-1">
                            <div class="col-6">
                                <input class="form-control" type="file" ref="dealersPictureRefEdit"
                                    @change="dealersEditPictureChange">
                            </div>
                            <div class="col-auto">
                                <img v-if="dealersEditImageUrl" :src="dealersEditImageUrl" style="max-height: 60px;"
                                    alt="">
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
                    Вы уверены, что хотите удалить "{{ dealerToDelete?.name }}"?
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
                    <h5 class="modal-title">Статистика Дилеров</h5>
                </div>
                <div class="modal-body">
                    <p>Количество Дилеров: {{ stats.count }}</p>
                    <p>Максимальный ID Дилера: {{ stats.max }}</p>
                    <p>Минимальный ID Дилера: {{ stats.min }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
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
    grid-template-columns: 1fr 1fr 1fr auto auto;
    align-items: center;
    gap: 18px;
}

.dealers-item img {
    cursor: pointer;
}
</style>