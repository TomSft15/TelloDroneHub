<template>
  <div class="home-container">
    <section class="hero">
      <div class="hero-content">
        <h1>Contrôlez votre drone de façon intuitive</h1>
        <p class="hero-description">
          Pilotez votre drone à l'aide de la voix, des gestes, de la vision ou du clavier. Une interface simple et puissante pour une expérience de vol optimale.
        </p>
        <div class="hero-buttons">
          <router-link to="/voice-control" class="btn-primary">
            <i class="fas fa-rocket"></i> Démarrer
          </router-link>
          <a href="#features" class="btn-outline">En savoir plus</a>
        </div>
      </div>
      <div class="hero-image">
      </div>
    </section>

    <section id="features" class="features">
      <h2 class="section-title">Plusieurs modes de contrôle</h2>
      <div class="feature-cards">
        <div class="feature-card">
          <div class="feature-icon voice-icon">
            <i class="fas fa-microphone"></i>
          </div>
          <h3>Contrôle vocal</h3>
          <p>Donnez des ordres à votre drone en utilisant simplement votre voix. Idéal pour garder les mains libres.</p>
          <router-link to="/voice-control" class="feature-link">Essayer <i class="fas fa-chevron-right"></i></router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon gesture-icon">
            <i class="fas fa-hand-paper"></i>
          </div>
          <h3>Contrôle gestuel</h3>
          <p>Pilotez votre drone avec des mouvements de main intuitifs capturés par votre caméra.</p>
          <router-link to="/gesture-control" class="feature-link">Essayer <i class="fas fa-chevron-right"></i></router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon vision-icon">
            <i class="fas fa-eye"></i>
          </div>
          <h3>Vision et suivi</h3>
          <p>Laissez votre drone suivre automatiquement des personnes ou des objets grâce à la reconnaissance visuelle.</p>
          <router-link to="/vision-control" class="feature-link">Essayer <i class="fas fa-chevron-right"></i></router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon keyboard-icon">
            <i class="fas fa-keyboard"></i>
          </div>
          <h3>Contrôle clavier</h3>
          <p>Utilisez votre clavier pour un contrôle précis et personnalisable de votre drone.</p>
          <router-link to="/keyboard-config" class="feature-link">Configurer <i class="fas fa-chevron-right"></i></router-link>
        </div>
      </div>
    </section>

    <section class="dashboard-preview">
      <div class="dashboard-content">
        <h2 class="section-title">Tableau de bord complet</h2>
        <p>Consultez en temps réel toutes les informations de vol de votre drone :</p>
        <ul class="dashboard-features">
          <li><i class="fas fa-battery-three-quarters"></i> Niveau de batterie</li>
          <li><i class="fas fa-signal"></i> Puissance du signal</li>
          <li><i class="fas fa-map-marker-alt"></i> Position GPS</li>
          <li><i class="fas fa-compass"></i> Orientation</li>
          <li><i class="fas fa-video"></i> Flux vidéo en direct</li>
        </ul>
        <router-link to="/dashboard" class="btn-primary">
          <i class="fas fa-tachometer-alt"></i> Voir le tableau de bord
        </router-link>
      </div>
      <div class="dashboard-image">
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
};
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Hero Section */
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem 0 4rem;
  gap: 3rem;
}

.hero-content {
  flex: 1;
}

.hero h1 {
  font-size: 2.8rem;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  color: var(--text-color);
  animation: fadeInUp 0.8s ease-out;
}

.hero-description {
  font-size: 1.2rem;
  color: var(--dark-gray);
  margin-bottom: 2rem;
  line-height: 1.6;
  animation: fadeInUp 1s ease-out;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  animation: fadeInUp 1.2s ease-out;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: var(--border-radius-md);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-outline {
  border: 2px solid var(--primary-color);
  color: var(--primary-color);
  padding: 0.8rem 1.5rem;
  border-radius: var(--border-radius-md);
  font-weight: 500;
  transition: all 0.3s ease;
  background-color: transparent;
}

.btn-outline:hover {
  background-color: var(--primary-color);
  color: white;
  transform: translateY(-2px);
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 50%;
  animation: float 6s ease-in-out infinite;
}

.hero-image img {
  max-width: 100%;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

/* Features Section */
.features {
  padding: 4rem 0;
}

.section-title {
  text-align: center;
  margin-bottom: 3rem;
  font-size: 2.2rem;
  color: var(--text-color);
  position: relative;
}

.section-title::after {
  content: '';
  display: block;
  width: 80px;
  height: 4px;
  background-color: var(--primary-color);
  margin: 1rem auto 0;
  border-radius: 2px;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background-color: white;
  border-radius: var(--border-radius-md);
  padding: 2rem;
  box-shadow: var(--card-shadow);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  color: white;
}

.voice-icon {
  background: linear-gradient(135deg, #3498db, #2980b9);
}

.gesture-icon {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.vision-icon {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
}

.keyboard-icon {
  background: linear-gradient(135deg, #9b59b6, #8e44ad);
}

.feature-card h3 {
  margin-bottom: 1rem;
  color: var(--text-color);
}

.feature-card p {
  color: var(--dark-gray);
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.feature-link {
  color: var(--primary-color);
  display: inline-flex;
  align-items: center;
  font-weight: 500;
  transition: all 0.2s ease;
}

.feature-link i {
  margin-left: 0.25rem;
  transition: transform 0.2s ease;
}

.feature-link:hover {
  color: var(--primary-dark);
}

.feature-link:hover i {
  transform: translateX(3px);
}

/* Dashboard Preview */
.dashboard-preview {
  padding: 5rem 0;
  display: flex;
  align-items: center;
  gap: 3rem;
  background-color: white;
  margin: 2rem 0;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--card-shadow);
  padding: 3rem;
}

.dashboard-content {
  flex: 1;
}

.dashboard-content .section-title {
  text-align: left;
  margin-bottom: 1.5rem;
}

.dashboard-content .section-title::after {
  margin: 1rem 0 0;
}

.dashboard-content p {
  color: var(--dark-gray);
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.dashboard-features {
  list-style: none;
  margin-bottom: 2rem;
}

.dashboard-features li {
  margin-bottom: 0.8rem;
  display: flex;
  align-items: center;
  color: var(--text-color);
}

.dashboard-features li i {
  color: var(--primary-color);
  margin-right: 0.8rem;
  font-size: 1.1rem;
}

.dashboard-image {
  flex: 1;
  max-width: 50%;
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.dashboard-image img {
  width: 100%;
  height: auto;
  display: block;
  border-radius: var(--border-radius-md);
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
}

/* Responsive Design */
@media screen and (max-width: 992px) {
  .hero {
    flex-direction: column-reverse;
    padding: 1rem 0 3rem;
  }
  
  .hero h1 {
    font-size: 2.2rem;
  }
  
  .hero-image {
    max-width: 90%;
    margin-bottom: 2rem;
  }
  
  .dashboard-preview {
    flex-direction: column;
    padding: 2rem;
  }
  
  .dashboard-image {
    max-width: 100%;
    order: -1;
    margin-bottom: 2rem;
  }
}

@media screen and (max-width: 768px) {
  .hero-description {
    font-size: 1rem;
  }
  
  .features {
    padding: 3rem 0;
  }
  
  .feature-cards {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>
