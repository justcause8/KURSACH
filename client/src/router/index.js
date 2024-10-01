import DealerCenterVue from '@/views/DealerCenterView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import DealerCenterView from '@/views/DealerCenterView.vue'
import DealerView from '@/views/DealerView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "DealerCenterView",
      component: DealerCenterView
    }, 
    {
      path: "/dealers",
      name: "DealerView",
      component: DealerView
    }
  ]
})

export default router
