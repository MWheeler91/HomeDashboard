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
                <!-- <button class="popup-close btn btn-danger mt-3" @click.prevent="resetData()"> -->
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
            this.errors = [];

            if (!this.data.email) this.errors.push('Your e-mail is missing')
            if (!this.data.password) this.errors.push('Your password is missing')

            if (this.errors.length > 0) return

            try {
                // 1. Attempt Login
                const response = await axios.post('/api/account/login/', this.data);
                this.userStore.setToken(response.data);

                // Ensure the token is retrieved correctly
                const token = this.userStore.user.access || localStorage.getItem("user.access");
                console.log("Retrieved Token:", token);

                if (!token) {
                    console.error("No token found! Unauthorized request.");
                    this.errors.push("Authentication Error: Missing token. Please log in again.");
                    return;
                }

                axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

                // 2. Fetch User Info
                const userResponse = await axios.get('/api/account/me/', {
                    headers: { 
                        Authorization: `Bearer ${token}`, 
                        "X-CSRFToken": document.cookie.split('csrftoken=')[1]?.split(';')[0] || "" 
                    },
                    withCredentials: true
                });

                this.userStore.setUserInfo(userResponse.data);

                // 3. Close Popup & Reload Page
                this.$emit('togglePopup');
                this.reloadPage();
            } catch (error) {
                if (error.message.includes("Network Error")) {
                    this.errors.push("Network Error: Unable to connect to server! Please try again later.");
                } else {
                    this.errors.push("Authentication Error: The email or password is incorrect or the user is not activated!");
                }
            }
        },
        resetData() {
            this.data = {
                email: "",
                password: ""
            }
        },
        reloadPage() {
            window.location.reload();
        },
    }
}
</script>