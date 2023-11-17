<template>
    <div class="row text-center px-3">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col" v-for="(label, key) in data.tableHeaders" @click="sortByHeader(key)">
                        {{ label }}
                    </th>
                    <th scope="col">Edit / Delete</th>

                </tr>
            </thead>
            <tbody>
                <tr v-for="(row, index) in sortedTableData" :key="index">
                    <td v-for="(value, key) in row" :key="key">
                        <span v-if="key === 'value' || key === 'cost'">{{ formatCurrency(row.value) }}</span>
                        <span v-else>{{ value }}</span>
                    </td>
                    <td>
                        <a class="btn btn-primary mx-2" @click="updateRow(row)">Edit</a>
                        <a class="btn btn-danger" @click="removeItemById(row.id)">Delete</a>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    name: "BaseTable",
    props: ['data'],
    data() {
        return {
            // default sorting values
            sortKey: "id",
            sortDirection: 1,
        }
    },
    computed: {
        sortedTableData() {
            // Check if a sorting key is specified
            if (this.sortKey) {
                // Use Array.prototype.sort() to sort the data based on the current key and direction
                return this.data.tableData.slice().sort((a, b) => {
                    const modifier = this.sortDirection;
                    const keyA = a[this.sortKey];
                    const keyB = b[this.sortKey];

                    if (!isNaN(keyA) && !isNaN(keyB)) {
                        // For numeric values
                        return (keyA - keyB) * modifier;
                    }

                    const strA = String(keyA).toLowerCase();
                    const strB = String(keyB).toLowerCase();
                    return strA.localeCompare(strB) * modifier;
                });
            }
            // If no sorting key is specified, return the original data
            return this.data.tableData;
        },
    },
    methods: {
        formatCurrency(value) {
            // Format the number as currency
            const formatter = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD' // Change to the appropriate currency code
            });

            // Use the formatter to format the value
            return formatter.format(value);
        },
        removeItemById(id) {
            this.$emit('delete-item', id)
        },
        updateRow(row) {
            this.$emit('update-row', row)
        },
        sortByHeader(key) {
            // Toggle sort direction if the same key is clicked again
            if (this.sortKey === key) {
                this.sortDirection *= -1;
            } else {
                // Set the new sorting key and reset direction to ascending
                this.sortKey = key;
                this.sortDirection = 1;
            }
        }


    }

}
</script>

<style scoped>
table {
    color: white;
    width: 100%;
    table-layout: fixed;
    vertical-align: middle;

}
</style>