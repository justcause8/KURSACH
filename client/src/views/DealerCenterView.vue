<script setup>
import { ref, computed, onBeforeMount } from 'vue';
import { storeToRefs } from 'pinia';
import axios from 'axios';
import _ from 'lodash';
import { Modal } from 'bootstrap'
import useUserStore from '../stores/userStore';

const dealer_centers = ref([]);
const dealers = ref({});
const dealercenterToAdd = ref({});
const dealercenterToEdit = ref({});
const confirmDeleteModalRef = ref();
const dealerCenterToDelete = ref(null);
const stats = ref({});
const userStore = useUserStore();
const { isSuperuser, users } = storeToRefs(userStore);

const filters = ref({
  headquarters_location: "",
  contact: "",
  manager: "",
  dealer_FK: "",
  user_id: ""
});

function onRemoveClick(dealercenter) {
  dealerCenterToDelete.value = dealercenter;
  const confirmModal = new Modal(confirmDeleteModalRef.value);
  confirmModal.show();
}

async function onConfirmDelete() {
  if (dealerCenterToDelete.value) {
    await axios.delete(`/api/dealer-centers/${dealerCenterToDelete.value.id}/`);
    await fetchDealerCenters();
  }
}

async function fetchDealerCenters() {
  const r = await axios.get("/api/dealer-centers/")
  debugLog('Dealer Centers', dealer_centers.value);
  dealer_centers.value = r.data;
}

async function fetchDealers() {
  const r = await axios.get("/api/dealers/")
  dealers.value = r.data;
}

async function onDealerCentersAdd() {
  await axios.post("/api/dealer-centers/", {
    ...dealercenterToAdd.value,
  });
  await fetchDealerCenters();
}

async function onDealerCentersEditClick(dealercenter) {
  dealercenterToEdit.value = {
    ...dealercenter,
    dealer_FK_id: dealercenter.dealer_FK.id,
  };
}

async function onDealerCenterUpdateClick() {
  await axios.put(`/api/dealer-centers/${dealercenterToEdit.value.id}/`, {
    ...dealercenterToEdit.value
  });
  await fetchDealerCenters();
}

async function fetchStats() {
  const r = await axios.get("/api/dealer-centers/stats/");
  stats.value = r.data;
}

// Фильтрация дилерских центров по введённым значениям
const filteredDealerCenters = computed(() => {
  const filtered = dealer_centers.value.filter(dealer => {
    const locationMatch = !filters.value.headquarters_location || dealer.headquarters_location.toLowerCase().includes(filters.value.headquarters_location.toLowerCase());
    const contactMatch = !filters.value.contact || dealer.contact.toLowerCase().includes(filters.value.contact.toLowerCase());
    const managerMatch = !filters.value.manager || dealer.manager.toLowerCase().includes(filters.value.manager.toLowerCase());
    const dealerMatch = !filters.value.dealer_FK || dealer.dealer_FK.id === filters.value.dealer_FK;
    const userMatch = !filters.value.user_id || dealer.user === filters.value.user_id;

    return locationMatch && contactMatch && managerMatch && dealerMatch && userMatch;
  });

  return filtered;
});

function resetFilters() {
  filters.value = {
    headquarters_location: "",
    contact: "",
    manager: "",
    dealer_FK: "",
    user_id: ""
  };
}

onBeforeMount(async () => {
  await userStore.fetchUser();
  if (isSuperuser.value) {
    await userStore.fetchUsers();
  }
  await fetchDealerCenters();
  await fetchDealers();
  await fetchStats();
});

</script>
<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onDealerCentersAdd">
        <h4>Ввод данных</h4>
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="dealercenterToAdd.headquarters_location" required>
              <label for="floatingInput">Location</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="dealercenterToAdd.contact" required>
              <label for="floatingInput">Contact</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="dealercenterToAdd.manager" required>
              <label for="floatingInput">Manager</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="dealercenterToAdd.dealer_FK_id" required>
                <option :value="d.id" v-for="d in dealers">{{ d.name }}</option>
              </select>
              <label for="floatingInput">Dealer</label>
            </div>
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
          <input type="text" class="form-control" placeholder="Location" v-model="filters.headquarters_location">
        </div>
        <div class="col">
          <input type="text" class="form-control" placeholder="Contact" v-model="filters.contact">
        </div>
        <div class="col">
          <input type="text" class="form-control" placeholder="Manager" v-model="filters.manager">
        </div>
        <div class="col">
          <select class="form-select" v-model="filters.dealer_FK">
            <option value="">Dealers</option>
            <option v-for="dealer in dealers" :key="dealer.id" :value="dealer.id">
              {{ dealer.name }}
            </option>
          </select>
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

      <div v-if="filteredDealerCenters.length > 0">
        <div v-for='item in filteredDealerCenters' class="dealercenters-item">
          <div>{{ item.headquarters_location }}</div>
          <div>{{ item.contact }}</div>
          <div>{{ item.manager }}</div>
          <div>{{ item.dealer_FK.name }}</div>

          <div class="d-flex justify-content-end">
            <button class="btn btn-success me-1" @click="onDealerCentersEditClick(item)" data-bs-toggle="modal"
              data-bs-target="#editDealerCenterModal">
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
                  <input type="text" class="form-control" v-model="dealercenterToEdit.headquarters_location">
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
              @click="onDealerCenterUpdateClick">Сохранить</button>
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
            Вы уверены, что хотите удалить "{{ dealerCenterToDelete?.headquarters_location }}"?
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
            <h5 class="modal-title">Статистика Дилерских центров</h5>
          </div>
          <div class="modal-body">
            <p>Количество Дилерских центров: {{ stats.count }}</p>
            <p>Максимальный ID Дилерского центра: {{ stats.max }}</p>
            <p>Минимальный ID Дилерского центра: {{ stats.min }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.dealercenters-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  box-shadow: 0 0 4px silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto auto auto auto;
  align-content: center;
  align-items: center;
  gap: 16px;
}
</style>