<template>
    <div class="dashboard-container">
      <div class="dashboard-header">
        <h1><i class="fas fa-tachometer-alt"></i> Tableau de bord du drone</h1>
        <div class="connection-status connected">
          <span class="status-indicator"></span>
          <span class="status-text">Connecté</span>
        </div>
      </div>
  
      <div class="dashboard-grid">
        <div class="camera-feed grid-item large">
          <div class="card-header">
            <h2>Flux vidéo en direct</h2>
            <div class="controls">
              <button class="btn-icon"><i class="fas fa-expand-alt"></i></button>
              <button class="btn-icon"><i class="fas fa-camera"></i></button>
            </div>
          </div>
          <div class="camera-content">
            <div class="camera-overlay">
              <div class="overlay-item altitude">300m</div>
              <div class="overlay-item speed">15m/s</div>
              <div class="overlay-item recording"><i class="fas fa-circle text-danger"></i> REC 00:03:45</div>
              <div class="overlay-item battery">
                <i class="fas fa-battery-half"></i> 68%
              </div>
            </div>
          </div>
        </div>
  
        <div class="flight-stats grid-item">
          <div class="card-header">
            <h2>Statistiques de vol</h2>
          </div>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-icon"><i class="fas fa-signal"></i></div>
              <div class="stat-value">98%</div>
              <div class="stat-label">Signal</div>
            </div>
            <div class="stat-item">
              <div class="stat-icon"><i class="fas fa-battery-three-quarters"></i></div>
              <div class="stat-value">68%</div>
              <div class="stat-label">Batterie</div>
            </div>
            <div class="stat-item">
              <div class="stat-icon"><i class="fas fa-temperature-high"></i></div>
              <div class="stat-value">32°C</div>
              <div class="stat-label">Température</div>
            </div>
            <div class="stat-item">
              <div class="stat-icon"><i class="fas fa-wind"></i></div>
              <div class="stat-value">8km/h</div>
              <div class="stat-label">Vent</div>
            </div>
          </div>
        </div>
  
        <div class="flight-data grid-item">
          <div class="card-header">
            <h2>Données de vol</h2>
          </div>
          <div class="data-table">
            <div class="data-row">
              <div class="data-label">Altitude</div>
              <div class="data-value">300 m</div>
            </div>
            <div class="data-row">
              <div class="data-label">Vitesse</div>
              <div class="data-value">15 m/s</div>
            </div>
            <div class="data-row">
              <div class="data-label">Distance</div>
              <div class="data-value">1.2 km</div>
            </div>
            <div class="data-row">
              <div class="data-label">Durée de vol</div>
              <div class="data-value">12:45</div>
            </div>
            <div class="data-row">
              <div class="data-label">Mode de vol</div>
              <div class="data-value">
                <span class="mode-badge">Auto</span>
              </div>
            </div>
          </div>
        </div>
  
        <div class="gps-location grid-item">
          <div class="card-header">
            <h2>Localisation GPS</h2>
            <button class="btn-icon toggle-map-type">
              <i class="fas fa-layer-group"></i>
            </button>
          </div>
          <div class="map-container">
            <div class="map-marker drone-marker">
              <i class="fas fa-drone-alt"></i>
            </div>
            <div class="map-marker home-marker">
              <i class="fas fa-home"></i>
            </div>
          </div>
          <div class="coordinates">
            <div>
              <span class="coordinate-label">Latitude</span>
              <span class="coordinate-value">48.8584° N</span>
            </div>
            <div>
              <span class="coordinate-label">Longitude</span>
              <span class="coordinate-value">2.2945° E</span>
            </div>
          </div>
        </div>
  
        <div class="recent-photos grid-item">
          <div class="card-header">
            <h2>Photos récentes</h2>
            <button class="btn-text">Voir toutes <i class="fas fa-chevron-right"></i></button>
          </div>
          <div class="photo-grid">
            <div class="photo-item">
            </div>
            <div class="photo-item">
            </div>
            <div class="photo-item">
            </div>
            <div class="photo-item">
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DashboardView'
  };
  </script>
  
  <style scoped>
  .dashboard-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 1rem;
  }
  
  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }
  
  .dashboard-header h1 {
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: var(--text-color);
  }
  
  .dashboard-header h1 i {
    color: var(--primary-color);
  }
  
  .connection-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    background-color: var(--light-gray);
  }
  
  .connection-status.connected {
    background-color: rgba(46, 204, 113, 0.2);
    color: #27ae60;
  }
  
  .connection-status .status-indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #27ae60;
    display: inline-block;
  }
  
  .dashboard-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 1.5rem;
  }
  
  .grid-item {
    background-color: white;
    border-radius: var(--border-radius-md);
    box-shadow: var(--card-shadow);
    overflow: hidden;
  }
  
  .large {
    grid-column: span 2;
    grid-row: span 2;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.25rem;
    background-color: var(--light-gray);
    border-bottom: 1px solid var(--medium-gray);
  }
  
  .card-header h2 {
    margin: 0;
    font-size: 1.1rem;
    color: var(--text-color);
    font-weight: 600;
  }
  
  .controls {
    display: flex;
    gap: 0.5rem;
  }
  
  .btn-icon {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    color: var(--dark-gray);
    border: 1px solid var(--medium-gray);
    transition: all 0.2s ease;
  }
  
  .btn-icon:hover {
    background-color: var(--light-gray);
    color: var(--primary-color);
  }
  
  .btn-text {
    background: none;
    border: none;
    color: var(--primary-color);
    font-size: 0.9rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.5rem;
    border-radius: var(--border-radius-sm);
  }
  
  .btn-text:hover {
    background-color: rgba(52, 152, 219, 0.1);
  }
  
  /* Camera Feed */
  .camera-content {
    position: relative;
    height: 100%;
  }
  
  .camera-content img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .camera-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  .overlay-item {
    background-color: rgba(0, 0, 0, 0.6);
    color: white;
    padding: 0.5rem 0.75rem;
    border-radius: var(--border-radius-sm);
    font-weight: 500;
    width: fit-content;
    font-family: 'Montserrat', sans-serif;
  }
  
  .overlay-item.altitude {
    align-self: flex-start;
  }
  
  .overlay-item.speed {
    align-self: flex-end;
  }
  
  .overlay-item.recording {
    align-self: flex-start;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .text-danger {
    color: #e74c3c;
  }
  
  .overlay-item.battery {
    align-self: flex-end;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  /* Stats */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    padding: 1rem;
    gap: 1rem;
  }
  
  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 1rem;
    background-color: var(--light-gray);
    border-radius: var(--border-radius-sm);
  }
  
  .stat-icon {
    font-size: 1.5rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
  }
  
  .stat-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 0.5rem;
  }
  
  .stat-label {
    font-size: 0.9rem;
    color: var(--dark-gray);
  }
  
  /* Flight Data */
  .data-table {
    padding: 1rem;
  }
  
  .data-row {
    display: flex;
    justify-content: space-between;
    padding: 0.8rem 0;
    border-bottom: 1px solid var(--light-gray);
  }
  
  .data-row:last-child {
    border-bottom: none;
  }
  
  .data-label {
    color: var(--dark-gray);
  }
  
  .data-value {
    font-weight: 500;
    color: var(--text-color);
  }
  
  .mode-badge {
    background-color: var(--primary-color);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: var(--border-radius-sm);
    font-size: 0.85rem;
  }
  
  /* GPS Location */
  .map-container {
    position: relative;
    height: 200px;
    overflow: hidden;
  }
  
  .map-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .map-marker {
    position: absolute;
    width: 24px;
    height: 24px;
    background-color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  }
  
  .drone-marker {
    top: 40%;
    left: 60%;
    color: var(--primary-color);
  }
  
  .home-marker {
    top: 60%;
    left: 30%;
    color: var(--accent-color);
  }
  
  .coordinates {
    display: flex;
    justify-content: space-between;
    padding: 1rem;
    font-size: 0.9rem;
  }
  
  .coordinate-label {
    color: var(--dark-gray);
    margin-right: 0.5rem;
  }
  
  .coordinate-value {
    font-weight: 500;
    color: var(--text-color);
  }
  
  /* Photos */
  .photo-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
    padding: 1rem;
  }
  
  .photo-item {
    border-radius: var(--border-radius-sm);
    overflow: hidden;
    aspect-ratio: 1;
  }
  
  .photo-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
  }
  
  .photo-item:hover img {
    transform: scale(1.05);
  }
  
  /* Responsive */
  @media screen and (max-width: 1200px) {
    .dashboard-grid {
      grid-template-columns: 1fr 1fr;
    }
    
    .large {
      grid-column: span 2;
    }
  }
  
  @media screen and (max-width: 768px) {
    .dashboard-grid {
      grid-template-columns: 1fr;
    }
    
    .large {
      grid-column: span 1;
    }
    
    .dashboard-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
  }
  </style>
  