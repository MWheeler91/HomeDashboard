<template>
    <div class="flex-container">
        <div class="row main-section app-card app-shadow my-3">
            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: "AppCardWrapper"
}
</script>

<style scoped>
.app-card{
    background-color: white;
    padding: 10px;
    border-radius: 15px;
    border: solid 2px;
    height: auto;
    width: auto;
}

.flex-container {
    flex: 1 1 0;
    width: 0;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    /* height: 150px; */
}
.app-shadow{
    box-shadow: rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(51, 51, 51) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px;
}
</style>