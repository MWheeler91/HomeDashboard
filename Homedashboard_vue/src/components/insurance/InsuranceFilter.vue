<template>
    <div class="d-flex">
        <div class="row  text-white text-center pt-4 align-items-center">
            <div class="col-md-1">
                <BaseFilterInput v-model="data.id" @filterChanged="updateFilter" :label="filteredTableData.tableHeaders.id"
                    :theKey="this.keyValues.id" :key="resetFlag" />
            </div>
            <div class="col-md-1">
                <BaseFilterInput v-model="data.item_name" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.item_name" :theKey="this.keyValues.item_name" :key="resetFlag" />
            </div>
            <div class="col-md-1">
                <BaseFilterInput v-model="data.item_description" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.item_description" :theKey="this.keyValues.item_description"
                    :key="resetFlag" />
            </div>
            <div class="col-md-1">
                <BaseFilterInput v-model="data.item_category" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.item_category" mode="select"
                    :options="this.form_options.category" :theKey="this.keyValues.item_category" :key="resetFlag" />
            </div>
            <div class="col-md-1">
                <BaseFilterInput v-model="data.condition" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.condition" mode="select" :options="this.form_options.condition"
                    :theKey="this.keyValues.condition" :key="resetFlag" />
            </div>
            <div class="col-md-1">
                <BaseFilterInput v-model="data.room" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.room" mode="select" :options="this.form_options.room"
                    :theKey="this.keyValues.room" :key="resetFlag" />
            </div>
            <div class="col-md-1">
                <BaseFilterInput v-model="data.value" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.value" :theKey="keyValues.value" :key="resetFlag" />
            </div>

            <div class="col-md-1">
                <BaseFilterInput v-model="data.serial_number" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.serial_number" :theKey="keyValues.serial_number"
                    :key="resetFlag" />
            </div>
            <div class="col-md-1">
                <BaseFilterInput v-model="data.model_number" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.model_number" :theKey="keyValues.model_number"
                    :key="resetFlag" />
            </div>

            <div class="col-md-1">
                <BaseFilterInput v-model="data.entered_by" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.date_entered" :theKey="this.keyValues.date_entered"
                    :key="resetFlag" />
            </div>
            <div class="col-md-1">
                <BaseFilterInput v-model="data.entered_by" @filterChanged="updateFilter"
                    :label="filteredTableData.tableHeaders.entered_by" :theKey="this.keyValues.entered_by"
                    :key="resetFlag" />
            </div>
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
    name: "InsuranceFilter",
    props: ['filteredTableData', 'tableData', 'form_options'],
    components: { BaseInput, BaseFilterInput },



    data() {
        return {
            data: {
                id: '',
                item_name: '',
                item_description: '',
                item_category: '',
                condition: '',
                room: '',
                value: '',
                serial_number: "",
                model_number: "",
                date_entered: '',
                entered_by: ''
            },
            keyValues: {
                id: "id",
                item_name: "item_name",
                item_description: "item_description",
                item_category: "item_category",
                condition: "condition",
                room: "room",
                value: "value",
                serial_number: "serial_number",
                model_number: "model_number",
                date_entered: "date_entered",
                entered_by: "entered_by"
            },
            empty_data: {
                id: '',
                item_name: '',
                item_description: '',
                item_category: '',
                condition: '',
                room: '',
                value: '',
                serial_number: "",
                model_number: "",
                date_entered: '',
                entered_by: ''
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
  