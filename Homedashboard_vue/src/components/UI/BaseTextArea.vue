<template>
    <label class="form-label">{{ label }}</label>
  <!--  If you passing an item from a parent to base-input then pass the mode otherwise you can omit mode.-->
  <!--  If you are passing a value from parent -> child -> base-input mode should not be included so the data emits correctly-->
    <textarea
            v-bind="$attrs"
            :placeholder="placeholder"
            class="field form-control mb-3"
            :value="modelValue"
            @input="$emit('update:modelValue', $event.target.value)"> 
    </textarea>
</template>

<script>
export default {
    name: "BaseTextArea",
    props: {
        label: {
            type: String,
            default: ""
        },
        modelValue: {
            type: [String, Number, Boolean],
            default: ""
        },
        placeholder: {
            type: [String, Number],
            default: ""
        },
        additionalLabel: {
            type: String,
            default: ""
        },
    },
    data() {
        return {
            value: ""
        }
    },
    methods: {
        setValue(v) {
            this.value = v
        },
        testvalue(e) {
            console.log("testing file value")
            console.log(e)
        }
    },
}
</script>

<style scoped>
.form-label {
    font-weight: bold;
}

textarea {
    border-style: solid;
    border-width: thin;
    border-color: black;
}
</style>