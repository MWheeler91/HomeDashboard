<template>
    <div class="container-fluid">
        <div class="row">
            <div class=" col-md-12">
                <MaintenanceFilter :filteredTableData="this.filteredTableData" :form_options="this.form_options"
                @filterChanged="filterTableData" @resetFilters="resetFilters" />
            </div>
        </div>


        <div class="row">
            <div class="col-md-12">
                <h4 class="text-center text-white">Total number of lines is {{ filteredTableLines }}</h4>
            </div>
        </div>
        <div class="row">
            <div class="">
                <vue-awesome-paginate :total-items="filteredTableLines" :items-per-page="itemsPerPage"
                    :max-pages-shown="maxPagesShown" v-model="currentPage" />

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
            <BaseTable :data="paginatedTableData" @delete-item="handleRemoveItem" @update-row="handelUpdateRow"
                :key="resetFlag" />
        </div>



    </div>
</template>

<script>
import { ref } from "vue";
import { useUserStore } from '@/store/user'
import axios from "axios";

import NewItem from "@/components/maintenance/NewItem.vue";
import EditItem from "@/components/maintenance/EditItem.vue";
import MaintenanceFilter from "@/components/maintenance/MaintenanceFilter.vue";



import BaseTable from "@/components/UI/BaseTable.vue";
import Popup from "@/components/UI/Popup.vue";

export default {
    name: 'MaintenanceHome',
    components: {
        BaseTable,
        MaintenanceFilter,
        Popup,
        NewItem,
        EditItem,
    },
    data () {
        return {
            data: {
                tableHeaders: {
                    id: "ID",
                    vehicle: "Vehicle",
                    category: "Category",
                    short_description: "Short Description",
                    maintenance_preformed: "Work Preformed",
                    mileage: "Mileage",
                    cost: "Cost",
                    date_preformed: "Date",
                    next_service: "Next Service Date",
                },
                tableData: []
            },
            filteredTableData: {
                tableHeaders: {
                    id: "ID",
                    vehicle: "Vehicle",
                    category: "Category",
                    short_description: "Short Description",
                    maintenance_preformed: "Work Preformed",
                    mileage: "Mileage",
                    cost: "Cost",
                    date_preformed: "Date",
                    next_service: "Next Service Date",
                },
                tableData: []
            },
            form_options: {
                vehicles: [],
                categories: []
            },
            vehicleStrings: [],
            resetFlag: 0,
            newItemTitle: "New Item",
            editItemTitle: "Edit Item",
            updateItemTitle: "Update Item",

            //pagination
            currentPage: 1,
            itemsPerPage: 50,
            maxPagesShown: 5,


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
    mounted() {
        this.getData()
    },
    methods: {
        // gets data from the item-list API
        async getData() {
            if (this.userStore.user.isAuthenticated) {
                axios
                    .get('/api/maintenance/maintenance-list', this.data.tableData)
                    .then(response => {
                        this.data.tableData = response.data
                        this.filteredTableData.tableData = response.data
                        console.log(response.data)
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
            axios
            .get('api/maintenance/get-values')
                .then((response) => {
                    this.form_options.vehicles = response.data.vehicle
                    this.form_options.categories = response.data.category
                })
                .catch(error => {
                    console.log(error)
                })
        },
        filterTableData(params) {
            // Initialize a copy of the tableData
            let filteredData = [...this.data.tableData];

            // Iterate over each key in the params object
            for (const filterKey in params) {
                if (Object.hasOwnProperty.call(params, filterKey)) {
                    const filterValue = params[filterKey].toString().toLowerCase();

                    // Apply the filter for the current key
                    filteredData = filteredData.filter(item => {
                        const itemValue = item[filterKey];
                        // Check if the item value is a number
                        if (typeof itemValue === 'number') {
                            // Convert the number to a string for comparison
                            return itemValue.toString().toLowerCase().includes(filterValue);
                        } else {
                            // Convert the item value to lowercase and check for inclusion
                            return itemValue.toString().toLowerCase().includes(filterValue);
                        }
                    });
                }
            }
            // Update the filteredTableData with the final result
            this.filteredTableData.tableData = filteredData;
            // Reset current page to 1 when filters change
            this.currentPage = 1;
        },
        handleRemoveItem(id) {
            axios
                .delete('/api/maintenance/delete-maintenance/' + id)
                .then((response) => {
                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error)
                })
            const updatedTableData = this.data.tableData.filter(item => item.id !== id);

            // this.resetFlag += 1
            this.data.tableData = updatedTableData
            this.filteredTableData.tableData = updatedTableData
            // this.resetFlag -= 1
        },
        // sets the pop up trigger to true and generates the edit item comp
        handelUpdateRow(row) {
            this.popupTriggers.editTrigger = true
            this.editItemData = row
        },
        resetFilters() {
            // this.getData()
            this.resetFlag += 1
            this.filteredTableData.tableData = this.data.tableData
            this.resetFlag -= 1

        }
    },
    computed: {
        filteredTableLines() {
            return this.filteredTableData.tableData.length;
        },
        TableLines() {
            return this.filteredTableData.tableData.length;
        },
        filteredTableDataLength() {
            return this.filteredTableData.tableData.length;
        },
        paginatedTableData() {
            let paginatedTableData =  {
                tableHeaders: {
                    id: "ID",
                    vehicle: "Vehicle",
                    category: "Category",
                    short_description: "Short Description",
                    maintenance_preformed: "Work Preformed",
                    mileage: "Mileage",
                    cost: "Cost",
                    date_preformed: "Date",
                    next_service: "Next Service Date"
                },
                tableData: []
            }
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            paginatedTableData.tableData = this.filteredTableData.tableData.slice(start, end);
            return paginatedTableData
        },
    }
}

</script>

<style scoped >

</style>