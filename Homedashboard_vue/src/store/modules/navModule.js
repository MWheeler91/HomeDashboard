export default {
    namespace: true,
    state() {
        return {
            first_name: "test",
            last_name : "test"
        }
    },
    mutations: {
        setUser(state, f_name, l_name){
            state.first_name = f_name
            state.last_name = l_name
        }
    },
    getters: {
        userName(state){
            return state.first_name
        }
    }
}