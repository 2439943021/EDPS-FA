<template>
  <div class="container">
    <el-dropdown
      @command="selectColor"
      @visible-change="toggleDropdown"
      trigger="click"
    >
      <el-button class="button">
        <div :style="{ backgroundColor: modelValue }" class="selected-color"></div>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item
            v-for="(presetColor, index) in presetColors"
            :key="index"
            :command="presetColor"
          >
            <div :style="{ backgroundColor: presetColor, width: '20px', height: '20px' }"></div>
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue';

interface ColorPickerProps {
  modelValue: string;
}

const { modelValue } = defineProps<ColorPickerProps>();
const emit = defineEmits(['update:modelValue']);

const isOpen = ref(false);

const presetColors = ref([
  '#FF0000', // 红色
  '#00FF00', // 绿色
  '#0000FF', // 蓝色
  // '#FFFF00', // 黄色
  '#FF00FF', // 品红
  '#00FFFF', // 青色
  '#FFA500', // 橙色
  '#FFD700', // 金色
  '#FF69B4', // 粉红
  '#FF6347', // 番茄红
]);

const toggleDropdown = (visible: boolean) => {
  isOpen.value = visible;
};

const selectColor = (selectedColor: string) => {
  emit('update:modelValue', selectedColor);
  isOpen.value = false;
};
</script>

<style scoped>
.container {
  text-align: center;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  cursor: pointer;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.selected-color {
  width: 20px;
  height: 20px;
  border: 1px solid #000;
}
</style>
