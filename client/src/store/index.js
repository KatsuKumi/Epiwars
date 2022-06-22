import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        challenge: {
            info: null,
            currentKata: null
        },
        auth: {
            user: null
        },
        ui: {
            showFooter: true
        }
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
        updateCurrentKata(state, kata) {
            state.challenge.currentKata = kata;
        },
        logout(state) {
            state.user = null
        },
        hideFooter(state) {
            state.ui.showFooter = false;
        },
        showFooter(state) {
            state.ui.showFooter = true;
        },
        updateCode(state, code) {
            state.challenge.currentKata.saved_code = code;
        },
        updateExample(state, code) {
            state.challenge.currentKata.saved_test = code;
        },
    },
    actions: {
        getCurrentKata: ({ commit }) => {
            return new Promise((resolve, reject) => {
                try {
                    axios.get('/api/kata/current/')
                        .then(response => { commit('updateCurrentKata', response.data); resolve(response.data); })
                        .catch(error => { console.log(error); reject(error); });
                } catch (error) {
                    console.log(error);
                    reject(error);
                }
            })
        },
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
        saveCode: async ({state, commit, dispatch}) => {
            try {
                axios.post('/api/kata/current/', {
                    code: state.challenge.currentKata.saved_code,
                    test: state.challenge.currentKata.saved_test
                }).then(response => {
                }).catch(err => {
                    console.log(err);
                })
            } catch (e) {
                console.log(e);
            }
        }
    },
    modules: {}
})
