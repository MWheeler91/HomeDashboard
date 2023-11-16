<template>
    <div class="container-fluid">

        <InsuranceFilter :filteredTableData="this.filteredTableData" :tableData="this.tableData"
            :form_options="this.form_options" @filterChanged="filterTableData" />




        <div class="row">
            <div class="col-md-12">
                <button class="btn btn-primary mt-3 float-end" @click="() => TogglePopup('buttonTrigger')">
                    New Item
                </button>
            </div>
        </div>


        <popup v-if="popupTriggers.buttonTrigger">
            <NewItem :title="this.newItemTitle" :form_options="this.form_options"
                :togglePopup="() => TogglePopup('buttonTrigger')" @getData="getData()" />
        </popup>
        <popup v-else-if="popupTriggers.editTrigger">
            <EditItem :title="this.editItemTitle" :form_options="this.form_options" :data="this.editItemData"
                @getData="getData()" :togglePopup="() => TogglePopup('editTrigger')" />
        </popup>


        <div class="col-md-12">
            <BaseTable :data="this.filteredTableData" @delete-item="handleRemoveItem" @update-row="handelUpdateRow" />
        </div>

    </div>
</template>

<script>
import { ref } from "vue";
import { useUserStore } from '@/store/user'
import axios from "axios";

import NewItem from "@/components/insurance/NewItem.vue";
import EditItem from "@/components/insurance/EditItem.vue";
import InsuranceFilter from "@/components/insurance/InsuranceFilter.vue";

// may not use these
import AppCard from "@/components/apps/AppCard.vue";
import AppCardWrapper from "@/components/apps/AppCardWrapper.vue";

import BaseTable from "@/components/UI/BaseTable.vue";

import Popup from "@/components/UI/Popup.vue";


export default {
    name: 'InsuranceHome',
    components: {
        BaseTable,
        InsuranceFilter,
        Popup,
        NewItem,
        EditItem,
        AppCard,
        AppCardWrapper,
        axios,

    },
    data() {
        return {
            // default values for "new item button".  This is not being used now.
            empty: {
                id: 999,
                app_name: 'Create New',
                web_address: 'nah',
                icon: './src/assets/plus.png'
            },
            // Data for the table
            data: {
                tableHeaders: {
                    id: "Item ID",
                    item_name: "Item Name",
                    item_description: "Item Description",
                    item_category: "Category",
                    condition: "Condition",
                    room: "Room",
                    value: "Value",
                    date_entered: "Date Entered",
                    entered_by: "Entered By"
                },
                tableData: []
            },
            filteredTableData: {
                tableHeaders: {
                    id: "Item ID",
                    item_name: "Item Name",
                    item_description: "Item Description",
                    item_category: "Category",
                    condition: "Condition",
                    room: "Room",
                    value: "Value",
                    date_entered: "Date Entered",
                    entered_by: "Entered By"
                },
                tableData: []
            },
            form_options: {
                category: [],
                room: [],
                condition: [],
            },

            newItemTitle: "New Item",
            editItemTitle: "Edit Item",
            updateItemTitle: "Update Item",

            // data prop of the item be edited to pass to the EditItem comp
            editItemData: {},
            // data prop for filtering the table

        }
    },
    setup() {
        // sets up access to the store and pop up triggers
        const userStore = useUserStore()
        const popupTriggers = ref({
            buttonTrigger: false,
            editTrigger: false,
            timedTrigger: false
        });

        const TogglePopup = (trigger) => {
            popupTriggers.value[trigger] = !popupTriggers.value[trigger]
        }
        return {
            popupTriggers,
            TogglePopup,
            userStore
        }
    },
    // Calls getData to fill table data var.
    mounted() {
        this.getData()


    },
    methods: {
        // gets data from the item-list API
        async getData() {
            if (this.userStore.user.isAuthenticated) {
                axios
                    .get('/api/catalog/item-list', this.data.tableData)
                    .then(response => {
                        this.data.tableData = response.data
                        this.filteredTableData.tableData = response.data

                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
            axios
                .get('api/catalog/get-values')
                .then((response) => {
                    this.form_options.category = response.data.category
                    this.form_options.room = response.data.room
                    this.form_options.condition = response.data.condition
                })
                .catch(error => {
                    console.log(error)
                })
        },
        // Filters the data.table data prop and updates the filter tabled prop
        filterTableData(params) {
            this.filteredTableData.tableData = this.data.tableData.filter(item =>
                item[params.filterKey].toLowerCase().includes(params.filterValue.toLowerCase()))
        },
        // sends delete request to the back end to delete the item from the backend then updates the tableData var
        handleRemoveItem(id) {
            axios
                .delete('/api/catalog/delete-item/' + id)
                .then((response) => {
                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error)
                })
            const updatedTableData = this.data.tableData.filter(item => item.id !== id);

            this.data.tableData = updatedTableData
            this.filteredTableData = updatedTableData
        },
        // sets the pop up trigger to true and generates the edit item comp
        handelUpdateRow(row) {
            this.popupTriggers.editTrigger = true
            this.editItemData = row
        },

    }
}
</script>

<style scoped>
table {
    color: white;
}
</style>