<template>
  <div class="home-view">
    <!-- Section Héro -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Contrôle intuitif de drone</h1>
        <p class="hero-subtitle">
          Une plateforme tout-en-un pour piloter votre drone via gestes, voix ou clavier
        </p>
        <div class="hero-actions">
          <router-link to="/dashboard" class="btn btn-primary">
            <font-awesome-icon icon="rocket" class="right-margin"/> Démarrer
          </router-link>
          <router-link to="/connect" class="btn btn-outline">
            <font-awesome-icon icon="plug" class="right-margin"/> Connecter un drone
          </router-link>
        </div>
      </div>
      <div class="hero-visual">
        <!-- Image du drone ou animation -->
        <div class="drone-animation">
          <div class="drone-body"></div>
          <div class="drone-propeller propeller-1"></div>
          <div class="drone-propeller propeller-2"></div>
          <div class="drone-propeller propeller-3"></div>
          <div class="drone-propeller propeller-4"></div>
        </div>
      </div>
    </section>
    
    <!-- Section Fonctionnalités -->
    <section class="features-section">
      <h2 class="section-title">Fonctionnalités intégrées</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <font-awesome-icon icon="tachometer-alt"/>
          </div>
          <h3>Tableau de bord unifié</h3>
          <p>Toutes les commandes et données en temps réel regroupées dans une interface intuitive</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <font-awesome-icon icon="hand-paper"/>
          </div>
          <h3>Contrôle gestuel</h3>
          <p>Pilotez votre drone avec des mouvements de main naturels capturés par votre caméra</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <font-awesome-icon icon="microphone"/>
          </div>
          <h3>Commandes vocales</h3>
          <p>Donnez des instructions à votre drone en utilisant simplement votre voix</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <font-awesome-icon icon="eye"/>
          </div>
          <h3>Suivi facial</h3>
          <p>Votre drone détecte et suit automatiquement des visages pour des prises de vue parfaites</p>
        </div>
      </div>
    </section>
    
    <!-- Section Interface -->
    <section class="interface-section">
      <div class="interface-content">
        <h2 class="section-title">Une interface intuitive</h2>
        <p class="section-description">
          Notre tableau de bord tout-en-un vous permet de basculer facilement entre différents modes de contrôle tout en visualisant les données de vol en temps réel.
        </p>
        <ul class="interface-features">
          <li><font-awesome-icon icon="check-circle" class="right-margin"/> Flux vidéo en direct</li>
          <li><font-awesome-icon icon="check-circle" class="right-margin"/> Statistiques détaillées du drone</li>
          <li><font-awesome-icon icon="check-circle" class="right-margin"/> Capture de photos et vidéos</li>
          <li><font-awesome-icon icon="check-circle" class="right-margin"/> Configuration personnalisable</li>
          <li><font-awesome-icon icon="check-circle" class="right-margin"/> Modes de contrôle interchangeables</li>
        </ul>
        <router-link to="/dashboard" class="btn btn-primary">
          <font-awesome-icon icon="desktop" class="right-margin"/> Explorer l'interface
        </router-link>
      </div>
      <div class="interface-preview">
        <div class="dashboard-mockup">
          <div class="mockup-header"></div>
          <div class="mockup-sidebar"></div>
          <div class="mockup-content">
            <div class="mockup-video"></div>
            <div class="mockup-controls"></div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Section Comment Démarrer -->
    <section class="getting-started-section">
      <h2 class="section-title">Comment démarrer</h2>
      <div class="steps-container">
        <div class="step-card">
          <div class="step-number">1</div>
          <h3>Connectez votre drone</h3>
          <p>Établissez une connexion avec votre drone Tello via WiFi</p>
          <router-link to="/connect" class="step-link">
            Guide de connexion<font-awesome-icon icon="arrow-right"/>
          </router-link>
        </div>
        
        <div class="step-card">
          <div class="step-number">2</div>
          <h3>Accédez au tableau de bord</h3>
          <p>Visualisez le flux vidéo et les données de vol en temps réel</p>
          <router-link to="/dashboard" class="step-link">
            Tableau de bord<font-awesome-icon icon="arrow-right"/>
          </router-link>
        </div>
        
        <div class="step-card">
          <div class="step-number">3</div>
          <h3>Choisissez votre mode de contrôle</h3>
          <p>Basculez entre contrôle manuel, gestuel, vocal ou suivi automatique</p>
          <router-link to="/dashboard" class="step-link">
            Modes de contrôle<font-awesome-icon icon="arrow-right"/>
          </router-link>
        </div>
      </div>
    </section>
    
    <!-- Section CTA -->
    <section class="cta-section">
      <div class="cta-content">
        <h2>Prêt à prendre les commandes ?</h2>
        <p>Lancez l'application et découvrez une nouvelle façon de piloter votre drone</p>
        <router-link to="/dashboard" class="btn btn-cta">
          Démarrer maintenant
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home-view {
  max-width: 100%;
  overflow-x: hidden;
}

/* Hero Section */
.hero-section {
  display: flex;
  align-items: center;
  min-height: 85vh;
  padding: 2rem;
  background: linear-gradient(135deg, #ebf4f5 0%, #c6e4f5 100%);
  position: relative;
  overflow: hidden;
}

.hero-content {
  flex: 1;
  max-width: 600px;
  z-index: 2;
  padding: 2rem;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.4rem;
  line-height: 1.6;
  color: #34495e;
  margin-bottom: 2.5rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.hero-visual {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 1;
}

/* Buttons */
.btn {
  padding: 0.8rem 1.8rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-primary {
  background-color: #3498db;
  color: white;
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
}

.btn-primary:hover {
  background-color: #2980b9;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(52, 152, 219, 0.4);
}

.btn-outline {
  background-color: transparent;
  color: #3498db;
  border: 2px solid #3498db;
}

.btn-outline:hover {
  background-color: rgba(52, 152, 219, 0.1);
  transform: translateY(-3px);
}

.btn-cta {
  background-color: #e74c3c;
  color: white;
  font-size: 1.1rem;
  padding: 1rem 2rem;
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
}

.btn-cta:hover {
  background-color: #c0392b;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(231, 76, 60, 0.4);
}

/* Drone Animation */
.drone-animation {
  position: relative;
  width: 300px;
  height: 300px;
}

.drone-body {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 30px;
  background-color: #34495e;
  border-radius: 15px;
}

.drone-propeller {
  position: absolute;
  width: 60px;
  height: 8px;
  background-color: #3498db;
  border-radius: 4px;
  animation: spin 0.3s linear infinite;
}

.propeller-1 {
  top: 30%;
  left: 20%;
}

.propeller-2 {
  top: 30%;
  right: 20%;
}

.propeller-3 {
  bottom: 30%;
  left: 20%;
}

.propeller-4 {
  bottom: 30%;
  right: 20%;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Features Section */
.features-section {
  padding: 5rem 2rem;
  background-color: #fff;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: #2c3e50;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -15px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background-color: #3498db;
  border-radius: 2px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background-color: #fff;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  width: 80px;
  height: 80px;
  background-color: #ebf4f5cb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: #3498db;
  font-size: 2rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.6;
}

/* Interface Section */
.interface-section {
  padding: 5rem 2rem;
  background-color: #f9f9f9;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.interface-content {
  flex: 1;
  min-width: 300px;
  padding: 2rem;
}

.interface-content .section-title {
  text-align: left;
}

.interface-content .section-title::after {
  left: 0;
  transform: none;
}

.section-description {
  color: #7f8c8d;
  line-height: 1.7;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.interface-features {
  list-style: none;
  padding: 0;
  margin-bottom: 2.5rem;
}

.interface-features li {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  color: #34495e;
  font-size: 1.1rem;
}

.interface-features li i {
  color: #2ecc71;
  margin-right: 1rem;
  font-size: 1.2rem;
}

.interface-preview {
  flex: 1;
  min-width: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.dashboard-mockup {
  width: 100%;
  max-width: 600px;
  height: 350px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

.mockup-header {
  height: 40px;
  background-color: #34495e;
  width: 100%;
}

.mockup-sidebar {
  position: absolute;
  width: 20%;
  height: calc(100% - 40px);
  top: 40px;
  left: 0;
  background-color: #ecf0f1;
}

.mockup-content {
  position: absolute;
  width: 80%;
  height: calc(100% - 40px);
  top: 40px;
  right: 0;
  display: flex;
  flex-direction: column;
}

.mockup-video {
  height: 60%;
  background-color: #95a5a6;
}

.mockup-controls {
  height: 40%;
  background-color: #ecf0f1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 10px;
  padding: 10px;
}

.mockup-controls::before {
  content: '';
  position: absolute;
  width: 30px;
  height: 30px;
  background-color: #3498db;
  border-radius: 5px;
  bottom: 20px;
  right: 30px;
}

/* Getting Started Section */
.getting-started-section {
  padding: 5rem 2rem;
  background-color: #fff;
}

.steps-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.step-card {
  flex: 1;
  min-width: 250px;
  max-width: 350px;
  background-color: #fff;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
}

.step-number {
  position: absolute;
  top: -30px;
  right: -30px;
  width: 100px;
  height: 100px;
  background-color: rgba(52, 152, 219, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #3498db;
  font-weight: 700;
  opacity: 0.7;
}

.step-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.step-card p {
  color: #7f8c8d;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.step-link {
  color: #3498db;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.step-link:hover {
  color: #2980b9;
  gap: 0.75rem;
}

/* CTA Section */
.cta-section {
  padding: 5rem 2rem;
  background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
  text-align: center;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta-section h2 {
  font-size: 2.5rem;
  color: white;
  margin-bottom: 1.5rem;
}

.cta-section p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.2rem;
  margin-bottom: 2.5rem;
}

/* Responsive */
@media (max-width: 992px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    padding-top: 5rem;
  }

  .hero-content {
    margin-bottom: 3rem;
  }

  .hero-title {
    font-size: 2.8rem;
  }

  .hero-actions {
    justify-content: center;
  }

  .interface-section {
    flex-direction: column;
    gap: 3rem;
  }

  .interface-content .section-title {
    text-align: center;
  }

  .interface-content .section-title::after {
    left: 50%;
    transform: translateX(-50%);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.2rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .step-card {
    min-width: 100%;
  }
}

@media (max-width: 480px) {
  .hero-actions {
    flex-direction: column;
    width: 100%;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .feature-card {
    padding: 1.5rem;
  }
}

.right-margin {
  margin-right: 10px;
}
</style>