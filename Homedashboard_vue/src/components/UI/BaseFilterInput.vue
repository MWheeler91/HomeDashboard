<template>
    <div v-if="mode === 'select'" class="col-md-12">
        <base-select v-model="data.filterValue" :label="this.label" class="" :options="this.options" @input="updateFilter()"
            required />
    </div>
    <div v-else class="col-md-12">
        <base-input v-model="data.filterValue" :label="this.label" type="text" class="" @input="updateFilter()" required />
    </div>
</template>
  
<script>
import BaseInput from "@/components/UI/BaseInput.vue";
import BaseSelect from "@/components/UI/BaseSelect.vue";



export default {
    name: "BaseFilterInput",
    props: ['label', 'mode', 'options', 'theKey'],
    components: { BaseInput, BaseSelect },



    data() {
        return {
            data: {
                filterKey: '',
                filterValue: '',
            }
        };
    },
    watch: {
        'data.filterValue': function (newValue, oldValue) {
            // Only trigger the updateFilter method if the value has actually changed
            if (newValue !== oldValue) {
                this.updateFilter();
            }
        },
    },
    methods: {
        updateFilter() {
            this.data.filterKey = this.theKey

            console.log("")
            console.log('--------Start BaseFilterInput --------')
            console.log(this.data)
            console.log('--------End BaseFilterInput --------')
            console.log("")
            // Emit the custom event to notify the parent about the filter change
            this.$emit('filterChanged', this.data);
        },
    },
};
</script>
  