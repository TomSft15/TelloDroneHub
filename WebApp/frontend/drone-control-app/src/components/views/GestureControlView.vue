<template>
    <div class="control-page">
      <div class="page-header">
        <h1><i class="fas fa-hand-paper"></i> Contrôle Gestuel</h1>
        <p class="page-description">Contrôlez votre drone avec des mouvements de mains captés par votre caméra.</p>
      </div>
      <ControlMode mode="gesture" />
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
  .control-page {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .page-header {
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--light-gray);
    padding-bottom: 1.5rem;
  }
  
  .page-header h1 {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: var(--text-color);
    margin-bottom: 0.75rem;
  }
  
  .page-header h1 i {
    color: var(--accent-color);
  }
  
  .page-description {
    color: var(--dark-gray);
    font-size: 1.1rem;
    max-width: 700px;
  }
  </style>
  