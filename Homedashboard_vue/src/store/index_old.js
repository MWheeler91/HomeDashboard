import { createStore } from 'vuex'

import navModule from './modules/navModule.js'


export default createStore({
    state:{
        isLoading: false,
        isAuthenticated: false,
        token: "",
        user: {
            id: 0,
            email: "",
            first_name: "",
            last_name : "",
            is_admin: false
        }

    },
    mutations: {
        initializeStore(state){
            if (localStorage.getItem('token')){
                state.token = localStorage.getItem('token')
                state.isAuthenticated = true
                state.user.id = localStorage.getItem('userid')
                state.user.email = localStorage.getItem('email')
                state.user.first_name = localStorage.getItem('first_name')
                state.user.last_name = localStorage.getItem('last_name')
                state.user.is_admin = localStorage.getItem('is_admin')
            } else {
                state.token = ""
                state.isAuthenticated = false
                state.user.id = 0
                state.user.email = ""
                state.user.first_name = ""
                state.user.last_name = ""
                state.user.is_admin = false
            }
            // remove later
            console.log("***** start user state - Remove later *****")
            console.log(state.user)
            console.log("***** end user state *****")
        },
        setIsLoading(state, status) {
            state.isLoading = status
        },
        setToken(state,token) {
            state.token = token
            state.isAuthenticated = true
        },
        removeToken(state){
            state.token = ''
            state.isAuthenticated = false
            state.user = {}
            localStorage.removeItem('token')
            localStorage.removeItem('userid')
            localStorage.removeItem('email')
            localStorage.removeItem('first_name')
            localStorage.removeItem('last_name')
            localStorage.removeItem('is_admin')

        },
        setUser(state, user){
            state.user = user
        }
    },
    actions: {

    },
    modules: {
        nav: navModule
    },
})