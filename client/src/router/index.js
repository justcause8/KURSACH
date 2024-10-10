import DealerCenterVue from '@/views/DealerCenterView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import DealerCenterView from '@/views/DealerCenterView.vue'
import DealerView from '@/views/DealerView.vue'
import CarsView from '@/views/CarsView.vue'
import SaleView from '@/views/SaleView.vue'
import CustomerView from '@/views/CustomerView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/dealer-centers",
      name: "DealerCenterView",
      component: DealerCenterView
    }, 
    {
      path: "/dealers",
      name: "DealerView",
      component: DealerView
    },
    {
      path: "/cars",
      name: "CarsView",
      component: CarsView
    },
    {
      path: "/sales",
      name: "SalesView",
      component: SaleView
    },
    {
      path: "/customers",
      name: "CustomerView",
      component: CustomerView
    },
  ]
})

export default router
