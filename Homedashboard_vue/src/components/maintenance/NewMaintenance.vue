<template>
    <div class="container">
        <h1 class="text-center">{{ title }}</h1>
        <form class="post-form p-3" method="POST" enctype="multipart/form-data" role="form">

            <div class="col-md-12">
                <div class="row">
                    <div class=" col-md-6">
                        <base-select v-model="data.vehicle" label="Vehicle" class=""
                        :options="this.form_options.vehicles" required />    
                    </div>       
                    <div class=" col-md-6">
                        <base-select v-model="data.category" label="Category" class=""
                        :options="this.form_options.category" required />         
                    </div>        
                </div>
                
            </div>




            <div class="col-md-12">
                <base-input v-model="data.short_description" label="Short Description" type="text" class="" required />
            </div>

            <!-- Needs to be updated to text area  -->
            <div class="col-md-12">
                <base-text-area v-model="data.maintenance_preformed" label="Maintenance Preformed" type="text" class="" required />
            </div>

            <div class="col-md-12">
                <div class="row">
                    <div class="col-md-6">
                        <base-input v-model="data.mileage" label="Mileage" type="number" class=""  />

                    </div>
                    <div class="col-md-6">
                        <base-input v-model="data.cost" label="Cost" type="number" class=""  />
                    </div>
                </div>
            </div>

            <div class="col-md-12">
                <div class="row">
                    <div class="col-md-6">
                        <base-input v-model="data.date_preformed" label="Date" type="date" class=""  />
                    </div>
                    <div class="col-md-6">
                        <base-input v-model="data.next_service" label="Next Service Date" type="date" class=""  />
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
import BaseTextArea from "@/components/UI/BaseTextArea.vue";


import axios from "axios";
import { useUserStore } from '@/store/user'


export default {
    name: "NewItem",
    props: ['togglePopup', 'title', 'form_options'],
    components: { BaseSelect, BaseInput, BaseCheckbox, BaseTextArea },
    data() {
        return {
            data: {
                vehicle: null,
                category: null,
                short_description: "",
                maintenance_preformed: "",
                mileage: "",
                cost: "",
                date_preformed: "",
                next_service: "",
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

            formData.append('vehicle', this.data.item_name)
            formData.append('category', this.data.item_description)
            formData.append('short_description', this.data.item_category)
            formData.append('maintenance_preformed', this.data.condition)
            formData.append('mileage', this.data.value)
            formData.append('cost', this.data.room)
            formData.append('date_preformed', this.data.model_number)
            formData.append('next_service', this.data.next_service)
            formData.append('person_id', this.userStore.user.id)

            console.log(formData)
            axios
                .post('api/maintenance/new-maintenance', this.data)
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