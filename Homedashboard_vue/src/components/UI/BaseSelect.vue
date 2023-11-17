<template>
  <label class="form-label">{{ label }}</label>
  <select v-bind="$attrs" class="field form-control mb-3" :value="this.selectedOption"
    @change="setSelectedValue($event.target.value), $emit('update:modelValue', $event.target.value)">
    <option value=" "></option>
    <option v-for="option in options" :value="option" :key="option" selected="">
      {{ option }}
    </option>
  </select>
</template>

<script>
export default {
  name: "BaseSelect",
  props: {
    label: {
      type: String,
      default: ""
    },
    modelValue: {
      type: [String, Number],
      default: ""
    },
    options: {
      type: Array
    },
  },

  data() {
    return {
      selectedOption: ""
    }
  },
  created() {
    this.selectedOption = this.modelValue
  },
  methods: {
    setSelectedValue(value) {
      this.selectedOption = value
    }
  }
}
</script>




<style scoped>
.form-label {
  font-weight: bold;
}

select {
  border-style: solid;
  border-width: thin;
  border-color: black;
}
</style>
