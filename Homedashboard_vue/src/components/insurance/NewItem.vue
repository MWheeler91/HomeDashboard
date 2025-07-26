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
                    <div class="col-md-6">
                        <base-input v-model="data.model_number" label="Model Number" type="text" class=""  />

                    </div>
                    <div class="col-md-6">
                        <base-input v-model="data.serial_number" label="Serial Number" type="text" class=""  />
                    </div>
                </div>
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
                    <div class="col-md-4">
                        <button class="popup-close btn btn-danger mt-3" @click.prevent="togglePopup()">Close
                        </button>
                    </div>
                    <div class="col-md-4 text-center mt-3">
                        <base-checkbox v-model="multiple_items" label="Inputing multiple items?" type="checkbox"
                            :labelBR="true" class="" required />
                    </div>
                    <!-- if the "Inputing multiple item checkbox is checked then use an alternate button that does not fully clear the form and close the pop up" -->
                    <!-- That way you can enter mutliple items without having to click the new item button everytime -->
                    <div class="col-md-4">
                        <button v-if="multiple_items" @click.prevent="submitForm();" class="btn btn-info mt-3 float-end">
                            Submit
                        </button>

                        <button v-else @click.prevent="submitForm(); togglePopup();" class="btn btn-primary mt-3 float-end">
                            Submit
                        </button>
                    </div>

                </div>
            </div>
            <div>
                <p>Checking the Multiple Items box does clear the form or close the pop-up upon submission</p>
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
    name: "NewItem",
    props: ['togglePopup', 'title', 'form_options'],
    components: { BaseSelect, BaseInput, BaseCheckbox },
    data() {
        return {
            data: {
                item_name: "",
                item_description: "",
                item_category: null,
                condition: null,
                room: null,
                serial_number: "",
                model_number: "",
                value: "",
                entered_by: this.userStore.user.id
            },
            multiple_items: false
        }
    },
    setup() {
        const userStore = useUserStore()
        return {
            userStore
        }
    },
    methods: {
        submitForm() {
            // create a form, append all the data, and send to the API to update an item
            const formData = new FormData()

            formData.append('item_name', this.data.item_name)
            formData.append('item_description', this.data.item_description)
            formData.append('item_category', this.data.item_category)
            formData.append('condition', this.data.condition)
            formData.append('value', this.data.value)
            formData.append('room', this.data.room)
            formData.append('model_number', this.data.model_number)
            formData.append('serial_number', this.data.serial_number)
            formData.append('person_id', this.userStore.user.id)

            console.log(formData)
            axios
                .post('api/catalog/new-item', this.data)
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