<template>
    <div class="container">
        <h1 class="text-center">Login</h1>
        <form class="post-form p-3" method="POST" enctype="multipart/form-data" role="form">
            <div class="col-md-12">
                <base-input v-model="data.email" label="Email" type="text" class="" placeholder="Your e-mail address"
                    required />
            </div>

            <div class="col-md-12 pt-3">
                <base-input v-model="data.password" label="Password" type="password" placeholder="Your password" class=""
                    required />
            </div>


            <div class="pt-3 text-danger" v-if="errors.length > 0">
                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>


            <button @click.prevent="submitForm();" class="btn btn-primary mt-3 float-end">
                Submit
            </button>
            <button class="popup-close btn btn-danger mt-3" @click.prevent="togglePopup(); resetData()">
                Close
            </button>



        </form>
    </div>
</template>

<script>
import BaseInput from "@/components/UI/BaseInput.vue";
import axios from "axios";
import { useUserStore } from '@/store/user'

export default {
    setup() {
        const userStore = useUserStore()
        return {
            userStore
        }
    },
    name: "LoginPage",
    props: ['togglePopup', 'getData'],
    components: { BaseInput },
    data() {
        return {
            data: {
                email: "",
                password: ""
            },
            errors: []
        }
    },
    methods: {
        async submitForm() {
            this.errors = []
            if (this.data.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.data.password === '') {
                this.errors.push('Your password is missing')
            }
            if (this.errors.length === 0) {
                await axios
                    .post('/api/account/login/', this.data)
                    .then(response => {
                        this.userStore.setToken(response.data)

                        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;
                    })
                    .catch(error => {
                        console.log('error', error)

                        this.errors.push('The email or password is incorrect! Or the user is not activated!')
                    })
            }
            if (this.errors.length === 0) {
                await axios
                    .get('/api/account/me/')
                    .then(response => {
                        this.userStore.setUserInfo(response.data)

                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
            this.reloadPage()
        },
        resetData() {
            this.data = {
                username: "",
                password: ""
            }
        },
        reloadPage() {
            window.location.reload();
        }
    }
}
</script>