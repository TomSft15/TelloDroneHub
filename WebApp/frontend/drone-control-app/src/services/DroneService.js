import axios from 'axios';

const API_URL = 'http://localhost:5000';

export default {
  connectDrone() {
    return axios.get(`${API_URL}/connect`);
  },
  
  getDroneData() {
    return axios.get(`${API_URL}/drone_data`);
  },
  
  takeoff() {
    return axios.get(`${API_URL}/takeoff`);
  },
  
  land() {
    return axios.get(`${API_URL}/land`);
  },
  
  move(direction, distance) {
    return axios.get(`${API_URL}/move/${direction}/${distance}`);
  },
  
  rotate(direction, angle) {
    return axios.get(`${API_URL}/rotate/${direction}/${angle}`);
  },
  
  getVideoUrl() {
    return `${API_URL}/video_feed?timestamp=${new Date().getTime()}`;
  }
};
