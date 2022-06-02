import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        challenge: {
            info: null
        },
        auth: {
            user: null
        },
    },
    getters: {
        isAuthenticated: state => {
            return state.auth.user !== null;
        }
    },
    mutations: {
        updateChallenge(state, challenge) {
            state.challenge.info = challenge;
        },
        updateUser(state, user) {
            state.auth.user = user;
        },
        logout(state) {
            state.user = null
        }
    },
    actions: {
        refreshCallenge: async ({state, commit, dispatch}) => {
            try {
                axios
                    .get('/api/challenge')
                    .then(response => (commit("updateChallenge", response.data)))
                    .catch(err => {
                        console.log("Error during user fetching");
                        commit('logout')
                    })
            } catch (e) {
                commit('logout')
            }
        },
        refreshUser: async ({state, commit, dispatch}) => {
            try {
                axios
                    .get('/api/me')
                    .then(response => (commit("updateUser", response.data)))
                    .catch(err => {
                        console.log("Error during user fetching");
                        commit('logout')
                    })
            } catch (e) {
                commit('logout')
            }
        },
    },
    modules: {}
})
