import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Challenge from '../views/Challenge.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Login page',
    component: Login
  },
  {
    path: '/home',
    name: 'Homepage',
    component: Home
  },
  {
    path: '/challenge',
    name: 'Challenge',
    component: Challenge
  }
]

const router = new VueRouter({
  mode: 'history',
  //base: process.env.BASE_URL,
  routes
})

export default router
