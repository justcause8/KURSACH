<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import { Modal } from 'bootstrap'

const dealers = ref([]);
const dealersToAdd = ref({
    name: '',
    headquarters_location: '',
});
const dealersToEdit = ref({
    name: '',
    headquarters_location: '',
    picture: '',
});
const dealersPictureRef = ref('');
const dealersPictureRefEdit = ref('');
const dealersAddImageUrl = ref('');
const dealersEditImageUrl = ref('');
const selectedImageUrl = ref();
const imageModalRef = ref();
const confirmDeleteModalRef = ref();
const dealerToDelete = ref(null);
const stats = ref({});

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
            'Content-Type': 'multipart/form-data'
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

onBeforeMount(async () => {
    await fetchDealers();
    await fetchStats();
});
</script>

<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent="onDealersAdd">
                <div class="row">
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

            <div v-for="item in dealers" class="dealers-item">
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