<template>
    <div class="container">
        <h1 class="text-center">{{ title }}</h1>
        <form class="post-form p-3" method="POST" enctype="multipart/form-data" role="form">
            <div class="col-md-12">
                <base-input v-model="data.item_name" label="Item Name" type="text" class="" required />
            </div>
            <div class="col-md-12">
                <base-input v-model="data.item_description" label="Item Description" type="text" class="" required />
            </div>
            <div class="col-md-12">
                <base-input v-model="data.value" label="Value" type="number" class="" required />
            </div>
            <div class="col-md-12">
                <div class="row">
                    <div class="col-md-4">
                        <base-select v-model="data.item_category" label="Item Category" class=""
                            :options="this.form_options.category" required />
                    </div>
                    <div class="col-md-4">
                        <base-select v-model="data.condition" label="Condition" class=""
                            :options="this.form_options.condition" required />
                    </div>
                    <div class="col-md-4">
                        <base-select v-model="data.room" label="Room" class="" :options="this.form_options.room" required />
                    </div>
                </div>
            </div>

            <div class="col-md-12">
                <div class="row">

                    <div class="col-md-6">
                        <button class="popup-close btn btn-danger mt-3" @click.prevent="togglePopup()">Close
                        </button>
                    </div>

                    <div class="col-md-6">

                        <button @click.prevent="submitForm(); togglePopup();" class="btn btn-primary mt-3 float-end">
                            Submit
                        </button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
import BaseInput from "@/components/UI/BaseInput.vue";
import BaseSelect from "@/components/UI/BaseSelect.vue";
import BaseCheckbox from "@/components/UI/BaseCheckbox.vue";

import axios from "axios";
import { useUserStore } from '@/store/user'


export default {
    name: "EditItem",
    props: ['togglePopup', 'title', 'data', 'form_options'],
    components: { BaseSelect, BaseInput, BaseCheckbox },
    data() {
        return {
            //  if true, do not close pop ups and do not clear the form when submitting
            multiple_items: false
        }
    },
    // gets access to the store
    setup() {
        const userStore = useUserStore()
        return {
            userStore
        }
    },
    methods: {
        // create a form, append all the data, and send to the API to update an item
        submitForm() {
            const formData = new FormData()

            formData.append('item_name', this.data.item_name)
            formData.append('item_description', this.data.item_description)
            formData.append('item_category', this.data.item_category)
            formData.append('condition', this.data.condition)
            formData.append('value', this.data.value)
            formData.append('room', this.data.room)
            formData.append('person_id', this.userStore.user.id)

            console.log(formData)
            axios
                .put('api/catalog/update-item/' + this.data.id, this.data)
                .then((response) => {
                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error)
                })
            // calls the getData function from the parent to update the table
            this.$emit('getData')
        },



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