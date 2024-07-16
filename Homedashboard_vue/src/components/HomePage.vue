<template>

    <div class="container-fluid">
        <div class="row center-screen">
            <div class="col-sm-12">
                <the-apps />
            </div>
        </div>
    </div>


</template>

<script>
import TheApps from "@/components/apps/TheApps.vue";
import NavBar from "@/components/layout/NavBar.vue";
import axios from "axios";
import { useUserStore } from '@/store/user'

export default {
    name: 'HomePage',
    components: {
        NavBar,
        TheApps
    },
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },
    beforeCreate() {
        this.userStore.initStore()

        const token = this.userStore.user.access

        if (token) {
            axios.defaults.headers.common["Authorization"] = "Bearer " + token;
        } else {
            axios.defaults.headers.common["Authorization"] = "";
        }
    }
}
</script>

<style>
/* .center-screen {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10%;
} */

body {
    background-color: #0f0f0f;
}
body{
  background-color: #d4d4d4;
}

 /*Remove number arrows*/
input[type=number].without_number::-webkit-inner-spin-button,
input[type=number].without_number::-webkit-outer-spin-button {
    -webkit-appearance: none;
     margin: 0;
}
</style>



