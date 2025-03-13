<template>
    <div>
      <h1>Vision Control</h1>
      <ControlMode mode="Vision" />
    </div>
  </template>
  
  <script>
  import ControlMode from '../ControlMode.vue';
  
  export default {
    components: {
      ControlMode,
    },
  };
  </script>
  
  <style scoped>
  h1 {
    color: #333;
  }
  </style>
  