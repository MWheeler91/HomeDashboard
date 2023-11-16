<template>
    <div class="row  text-white text-center pt-4">
        <div class="col-md-1">
            <BaseFilterInput v-model="data.filterValue" @filterChanged="updateFilter"
                :label="filteredTableData.tableHeaders.id" 
                :theKey="this.keyValues.id" />
        </div>
        <div class="col-md-2">
            <BaseFilterInput v-model="data.filterValue" @filterChanged="updateFilter"
                :label="filteredTableData.tableHeaders.item_name" 
                :theKey="this.keyValues.item_name" />
        </div>
        <div class="col-md-2">
            <BaseFilterInput v-model="data.filterValue" @filterChanged="updateFilter"
                :label="filteredTableData.tableHeaders.item_description" 
                :theKey="this.keyValues.item_description" />
        </div>
        <div class="col-md-1">
            <BaseFilterInput v-model="data.filterValue" @filterChanged="updateFilter"
                :label="filteredTableData.tableHeaders.item_category" mode="select" :options="this.form_options.category"
                :theKey="this.keyValues.item_category" />
        </div>
        <div class="col-md-1">
            <BaseFilterInput v-model="data.filterValue" @filterChanged="updateFilter"
                :label="filteredTableData.tableHeaders.condition" mode="select" :options="this.form_options.condition"
                :theKey="this.keyValues.condition" />
        </div>
        <div class="col-md-1">
            <BaseFilterInput v-model="data.filterValue" @filterChanged="updateFilter"
                :label="filteredTableData.tableHeaders.room" mode="select" :options="this.form_options.room" 
                :theKey="this.keyValues.room" />
        </div>
        <div class="col-md-1">
            <BaseFilterInput v-model="data.filterValue" @filterChanged="updateFilter"
                :label="filteredTableData.tableHeaders.value" 
                :theKey="keyValues.value" />
        </div>
        <div class="col-md-1">
            <BaseFilterInput v-model="data.filterValue" @filterChanged="updateFilter"
                :label="filteredTableData.tableHeaders.date_entered" 
                :theKey="this.keyValues.date_entered" />
        </div>
        <div class="col-md-1">
            <BaseFilterInput v-model="data.filterValue" @filterChanged="updateFilter"
                :label="filteredTableData.tableHeaders.entered_by" 
                :theKey="this.keyValues.entered_by" />
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
                filterKey: '',
                filterValue: '',
            },
            keyValues: {
                id: "id",
                item_name: "item_name",
                item_description: "item_description",
                item_category: "item_category",
                condition: "condition",
                room: "room",
                value: "value",
                date_entered: "date_entered",
                entered_by: "entered_by"
            }
        };
    },
    methods: {
        updateFilter(value) {
            this.data.filterKey = value.filterKey
            this.data.filterValue = value.filterValue

            console.log()
            console.log('-------- Start Insurance Filter --------')
            console.log(value)
            console.log(this.data)
            console.log('--------End Insurance Filter --------')
            console.log()

            // console.log("Insurance Filter :" + this.filterValue)
            // Emit the custom event to notify the parent about the filter change
            this.$emit('filterChanged', this.data);
        },
    },
};
</script>
  