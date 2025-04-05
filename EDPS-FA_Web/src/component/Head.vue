<template>
    <div style="background-color: #f0f0f0;">
        <el-page-header @back="goBack">
        <template #content>
            <span class="text-large font-600 mr-3"> Title </span>
        </template>
        </el-page-header>    
    </div>
    
</template>

<script setup lang="ts" name="head">
    const goBack = () => {
        console.log('go back')
    }
</script>

<style scoped>

</style>