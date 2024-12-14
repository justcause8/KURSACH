import { createRouter, createWebHistory } from 'vue-router'
import DealerCenterView from '@/views/DealerCenterView.vue'
import DealerView from '@/views/DealerView.vue'
import CarsView from '@/views/CarsView.vue'
import SaleView from '@/views/SaleView.vue'
import CustomerView from '@/views/CustomerView.vue'
import LoginView from '@/views/LoginView.vue'
// import TradeInView from '@/views/TradeInView.vue'

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
    {
      path: "/login",
      name: "LoginView",
      component: LoginView
    },
  ]
})

export default router
