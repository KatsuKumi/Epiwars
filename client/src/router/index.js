import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Challenge from '../views/Challenge.vue'
import Panel from '../views/Panel/Panel.vue'
import Katas from '../views/Panel/Katas.vue'
import Challenges from '../views/Panel/Challenges.vue'
import Ranking from '../views/Ranking.vue'
//import Users from '../views/Panel/Users.vue'
import Settings from '../views/Panel/Settings.vue'

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
  },
  {
    path: '/ranking',
    name: 'Ranking',
    component: Ranking
  },
  {
    path: '/panel/',
    name: 'Panel',
    redirect: '/panel/dashboard',
  },
  {
    path: '/panel/dashboard',
    name: 'Admin panel',
    component: Panel
  },
  {
    path: '/panel/challenges',
    name: 'Challenges list',
    component: Challenges
  },
  {
    path: '/panel/katas',
    name: 'Katas list',
    component: Katas
  },
  {
    path: '/panel/settings',
    name: 'Settings',
    component: Settings
  }
]

const router = new VueRouter({
  mode: 'history',
  //base: process.env.BASE_URL,
  routes
})

export default router
