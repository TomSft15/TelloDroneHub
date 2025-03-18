<template>
  <header class="navbar">
    <div class="navbar-container">
      <div class="navbar-logo">
        <router-link to="/">
          <span class="logo-text">Drone Control</span>
        </router-link>
      </div>

      <button class="mobile-menu-toggle" @click="toggleMobileMenu">
        <span></span>
        <span></span>
        <span></span>
      </button>

      <nav class="navbar-links" :class="{ 'is-active': mobileMenuOpen }">
        <router-link to="/" @click="closeMobileMenu">Accueil</router-link>
        <router-link to="/dashboard" @click="closeMobileMenu">
          <i class="fas fa-tachometer-alt"></i> Tableau de bord
        </router-link>
        <router-link to="/connect" @click="closeMobileMenu">
          <i class="fas fa-wifi"></i> Connecter un drone
        </router-link>
        <router-link to="/keyboard-config" @click="closeMobileMenu">
          <i class="fas fa-keyboard"></i> Configuration du clavier
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      mobileMenuOpen: false
    };
  },
  methods: {
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen;
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false;
    }
  }
};
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #2c3e50, #1a252f);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  max-width: 1300px;
  margin: 0 auto;
}

.navbar-logo a {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
}

.logo-img {
  width: 32px;
  height: 32px;
  margin-right: 0.5rem;
}

.logo-text {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.25rem;  
  font-weight: 600;
}

.navbar-links {
  display: flex;
  gap: 0.5rem;
}

.navbar-links a {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius-sm);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  font-family: 'Montserrat', sans-serif;
}

.navbar-links a i {
  margin-right: 0.5rem;
}

.navbar-links a:hover {
  color: white;
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.navbar-links a.router-link-exact-active {
  color: white;
  background-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2);
}

.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 30px;
  height: 21px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 10;
}

.mobile-menu-toggle span {
  width: 30px;
  height: 3px;
  background-color: white;
  border-radius: 10px;
  transition: all 0.3s ease-in-out;
}

@media screen and (max-width: 768px) {
  .mobile-menu-toggle {
    display: flex;
  }

  .navbar-links {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background-color: #2c3e50;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding-top: 5rem;
    transition: transform 0.3s ease-in-out;
    transform: translateY(-100%);
    z-index: 5; 
  }

  .navbar-links.is-active {
    transform: translateY(0);
  }

  .navbar-links a {
    margin: 0.5rem 0;
    font-size: 1.25rem;
  }
}
</style>