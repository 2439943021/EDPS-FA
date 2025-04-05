<template>
  <div class="color-picker">
    <!-- <h1>颜色选择器</h1> -->
    <input type="color" v-model="colorValue" />
    <div class="color-box" :style="{ backgroundColor: colorValue, width: '20px', height: '20px' }"></div>
    <!-- <p>当前颜色: {{ colorValue }}</p> -->
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';

const props = defineProps({
  modelValue: String
});

const emits = defineEmits(['update:modelValue']);

const colorValue = ref(props.modelValue);

watch(colorValue, (newValue) => {
  emits('update:modelValue', newValue);
});
</script>

<style scoped>
.color-picker {
  text-align: center;
  font-family: Arial, sans-serif;
}

.color-box {
  width: 200px;
  height: 200px;
  margin: 20px auto;
  border: 1px solid #000;
}
</style>
