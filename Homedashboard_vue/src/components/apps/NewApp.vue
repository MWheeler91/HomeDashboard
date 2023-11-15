<template>
    <div class="container">
        <h1 class="text-center">Add new Service</h1>
        <form class="post-form p-3" method="POST" enctype="multipart/form-data" role="form">
            <div class="col-md-12">
                <base-input v-model="data.app_name" label="App Name" type="text" class="" required />
            </div>

            <div class="col-md-12">
                <base-input v-model="data.web_address" label="Web Address" type="text" class="" required />
            </div>


            <div class="col-md-12">
                <label class="form-label">Icon</label>
                <input type="file" @change="getImage($event)" class="field form-control mb-3" />
            </div>

            <div class="col-md-12">
                <div class="row">
                    <div class="col-md-6">
                        <base-checkbox v-model="data.is_vue_app" label="Vue App?" type="checkbox" class="" required />
                    </div>
                    <div class="col-md-6 float-end">
                        <base-checkbox v-model="data.login_required" label="Login Required?" type="checkbox" class=""
                            required />
                    </div>
                </div>

            </div>

            <div class="col-md-12">
                <button class="popup-close btn btn-danger mt-3"
                    @click.prevent="togglePopup(); resetData($event.target.files[0])">Close
                </button>
                <button @click.prevent="submitForm(); togglePopup(); getData();" class="btn btn-primary mt-3 float-end">
                    Submit
                </button>

            </div>

        </form>
<!-- 
               <div>
                   <h1>-&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45; Testing -&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;</h1>
                   <h5>{{ data }}</h5>
                   <h1>-&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45; End Testing -&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;</h1>
               </div> -->
    </div>
</template>

<script>
import BaseInput from "@/components/UI/BaseInput.vue";
import BaseCheckbox from "@/components/UI/BaseCheckbox.vue";
import axios from "axios";
// import FileInput from "@/components/UI/FileInput.vue";

export default {
    name: "NewApp",
    props: ['togglePopup', 'getData'],
    components: { BaseCheckbox, BaseInput },
    data() {
        return {
            data: {
                app_name: "",
                web_address: "",
                icon: "",
                prefix: "",
                login_required: false,
                is_vue_app: false
            },
        }
    },
    methods: {
        submitForm() {
            const formData = new FormData()

            formData.append('app_name', this.data.app_name)
            formData.append('web_address', this.data.web_address)
            formData.append('icon', this.data.icon)
            formData.append('login_required', this.data.login_required)
            formData.append('is_vue_app', this.data.is_vue_app)

            axios
                .post('apps/applist/', formData)
                .then((response) => {
                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error)
                })
                this.reloadPage()
        },
        resetData() {
            this.data = {
                app_name: "",
                web_address: "",
                icon: "",
                prefix: "",
                login_required: false,
                is_vue_app: false
            }
        },
        getImage(event) {
            this.data.icon = event.target.files[0]
        },
        reloadPage() {
            window.location.reload();
        }
    
    }
}
</script>

<style scoped>
.form-label {
    font-weight: bold;
}

input {
    border-style: solid;
    border-width: thin;
    border-color: black;
}
</style>