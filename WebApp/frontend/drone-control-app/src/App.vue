<template>
  <div id="app">
    <Navbar />
    <main class="main-content">
      <router-view/>
    </main>
    <footer class="app-footer">
      <p>© 2025 Drone Control System | Conçu avec ❤️ pour les pilotes</p>
    </footer>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  created() {
    localStorage.removeItem('droneImages')
  },
  components: {
    Navbar,
  }
};
</script>

<style>
/* Importation de polices Google pour un design plus moderne */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Roboto:wght@300;400;500&display=swap');

:root {
  /* Palette de couleurs principale */
  --primary-color: #3498db;
  --primary-dark: #2980b9;
  --accent-color: #e74c3c;
  --success-color: #2ecc71;
  --warning-color: #f39c12;
  --bg-color: #f8f9fa;
  --text-color: #333;
  --light-gray: #ecf0f1;
  --medium-gray: #bdc3c7;
  --dark-gray: #7f8c8d;
  --card-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  
  /* Espacement */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  
  /* Bordures */
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Roboto', sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
  line-height: 1.6;
  margin: 0;
  padding: 0;
  min-height: 100vh;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  margin-bottom: var(--spacing-md);
}

h1 {
  font-size: 2.2rem;
  color: var(--primary-dark);
}

h2 {
  font-size: 1.8rem;
  color: var(--primary-color);
}

h3 {
  font-size: 1.5rem;
  color: var(--text-color);
}

p {
  margin-bottom: var(--spacing-md);
}

a {
  color: var(--primary-color);
  text-decoration: none;
  transition: all 0.2s ease;
}

a:hover {
  color: var(--primary-dark);
}

button {
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: var(--border-radius-md);
  background-color: var(--primary-color);
  color: white;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
}

button:active {
  transform: translateY(0);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.card {
  background: white;
  border-radius: var(--border-radius-md);
  box-shadow: var(--card-shadow);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.main-content {
  min-height: calc(100vh - 140px); /* Hauteur - (header + footer) */
  padding: var(--spacing-xl);
}

.app-footer {
  background-color: var(--dark-gray);
  color: white;
  text-align: center;
  padding: var(--spacing-md);
  margin-top: auto;
}

/* Styles responsive */
@media (max-width: 768px) {
  h1 {
    font-size: 1.8rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  h3 {
    font-size: 1.2rem;
  }
  
  .main-content {
    padding: var(--spacing-md);
  }
}
</style>
