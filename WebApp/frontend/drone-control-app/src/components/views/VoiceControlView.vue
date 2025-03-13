<template>
    <div>
      <h1>Voice Control</h1>
      <ControlMode mode="Voice" />
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
  