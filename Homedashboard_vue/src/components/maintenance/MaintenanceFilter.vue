<template>
    <div class="d-flex">
        <div class="row  text-white text-center pt-4 align-items-center">
            <div class="col-md-1">
                <BaseFilterInput v-model="data.id" @filterChanged="updateFilter" :label="filteredTableData.tableHeaders.id"
                    :theKey="this.keyValues.id" :key="resetFlag" />
            </div>

            <div class="col-md-1">
                <BaseFilterInput 
                    v-model="data.vehicle" 
                    @filterChanged="updateFilter" 
                    :label="filteredTableData.tableHeaders.vehicle" 
                    mode="select" 
                    :options="this.form_options.vehicles"
                    :theKey="this.keyValues.vehicle" 
                    :key="resetFlag" />
            </div>

            <div class="col-md-1">
                <BaseFilterInput 
                    v-model="data.category" 
                    @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.category" 
                    mode="select" 
                    :options="this.form_options.category"
                    :theKey="this.keyValues.category" 
                    :key="resetFlag" />
            </div>


            <div class="col-md-1">
                <BaseFilterInput v-model="data.short_description" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.short_description" :theKey="this.keyValues.short_description" :key="resetFlag" />
            </div>
            <div class="col-md-4">
                <BaseFilterInput v-model="data.maintenance_preformed" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.maintenance_preformed" :theKey="this.keyValues.maintenance_preformed"
                    :key="resetFlag" />
            </div>


            <div class="col-md-1">
                <BaseFilterInput v-model="data.mileage" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.mileage" 
                     :theKey="this.keyValues.mileage" :key="resetFlag" />
            </div>
            <div class="col-md-1">
                <BaseFilterInput v-model="data.cost" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.cost" 
                    :theKey="this.keyValues.cost" :key="resetFlag" />
            </div>
            <div class="col-md-1">
                <BaseFilterInput v-model="data.date_preformed" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.date_preformed" 
                    :theKey="this.keyValues.date_preformed" :key="resetFlag" />
            </div>

<!-- 
            <div class="col-md-1">
                <BaseFilterInput v-model="data.next_service" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.next_service" :theKey="keyValues.next_service" :key="resetFlag" />
            </div> -->




            <div class="col-md-1">
                <a class="btn btn-secondary align-center" @click="resetTable()">Clear Filters</a>
            </div>

        </div>
    </div>
</template>
  
<script>
import BaseInput from "@/components/UI/BaseInput.vue";
import BaseFilterInput from "@/components/UI/BaseFilterInput.vue";


export default {
    name: "MaintenanceFilter",
    props: ['filteredTableData', 'tableData', 'form_options'],
    components: { BaseInput, BaseFilterInput },



    data() {
        return {
            data: {
                id: '',
                vehicle: '',
                category: '',
                short_description: '',
                maintenance_preformed: '',
                mileage: '',
                cost: '',
                date_preformed: '',
                next_service: ''
            },
            keyValues: {
                id: "id",
                vehicle: "vehicle",
                category: "category",
                short_description: "short_description",
                maintenance_preformed: "maintenance_preformed",
                mileage: "mileage",
                cost: "cost",
                date_preformed: "date_preformed",
                next_service: "next_service"
            },
            empty_data: {
                id: '',
                vehicle: '',
                category: '',
                short_description: '',
                maintenance_preformed: '',
                mileage: '',
                cost: '',
                date_preformed: '',
                next_service: ''
            },
            resetFlag: 0,
        };
    },
    methods: {
        updateFilter(value) {
            this.data[value.filterKey] = value.filterValue
            // Emit the custom event to notify the parent about the filter change
            this.$emit('filterChanged', this.data);
        },
        resetTable() {

            // Manually clear the values of input and select boxes
            for (const key in this.data) {
                if (Object.hasOwnProperty.call(this.data, key)) {
                    this.data[key] = ''; // Clear the value
                }
            }
            this.resetFlag += 1;

            this.resetFlag -= 0

            this.$emit('resetFilters');
        }
    },
};
</script>

<style>
hr {
    border: none;
    height: 50px;
    background-color: white;
    /* width: 50px; */
}

.test {
    height: auto;
}
</style>
  