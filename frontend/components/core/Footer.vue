<template>
    <div class="footer">by Caio Graça Melo, {{ currentYear }}</div>
</template>
<style scoped>
.footer {
    color: rgba(203, 213, 225, 0.95);
    position: absolute;
    bottom: 0px;
    padding: 0px 12px;
    display: flex;
    justify-content: flex-end;
}
</style>
<script>
export default {
    computed: {
        currentYear() {
            return new Date().getFullYear();
        },
    },
};
</script>