# TelloDroneHub Project

## Overview

This project involves programming a **Tello DJI drone** to perform various interactive tasks. These include voice-controlled flight, gesture-controlled flight, facial recognition, and automatic face tracking. Additionally, a web application is developed to store and display data collected by the drone, such as photos, identified individuals, and performance statistics.

### Functional Purpose
As a developer or user, the goal is to control and use the drone intuitively and hands-free through:

- **Voice commands** (e.g., "take off," "land," "move forward")
- **Gesture recognition** (e.g., hand signals for movement commands)
- **Facial recognition** (for detecting and tracking individuals)

The web application allows users to:
- View and manage photos captured by the drone
- Access a list of individuals identified through facial recognition
- Visualize drone performance statistics

---

## Features

### Drone Functionalities
1. **Voice-Controlled Flight**
   - Commands: take off, land, move, stop
   - Implemented with Python using the Tello SDK and SpeechRecognition library

2. **Gesture-Controlled Flight**
   - Utilizes OpenCV and Mediapipe to detect and interpret hand gestures

3. **Facial Recognition**
   - Detects and identifies faces using AI models

4. **Face Detection and Automatic Tracking**
   - Automatically follows a detected face, adjusting the drone’s movement in real time

### Web Application Functionalities
1. **Photo Gallery**
   - Display photos captured by the drone
   - Filter by date and location
   - Download options for users

2. **Facial Recognition Data**
   - List of detected individuals with timestamps and locations
   - Search functionality

3. **Performance Statistics**
   - Number of flights, take-offs, landings, photos, and battery usage
   - Distance traveled and total flight time

4. **Admin Dashboard**
   - Manage drone data (upload, edit, delete entries)
   - Configure drone settings and API integrations

5. **Graphical Reports**
   - Visualize statistics with bar charts and pie charts for flights, battery usage, and photos

---

## Technology Stack

- **Drone**: Tello DJI with built-in camera
- **Programming Languages**: Python, JavaScript, SQL
- **Front-end Framework**: React
- **Back-end**: Node.js (or other server technology)
- **Database**: SQL (MySQL, PostgreSQL, or equivalent)
- **APIs and Libraries**:
  - Tello SDK (https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf)
  - OpenCV (https://opencv.org/)
  - SpeechRecognition Library (https://pypi.org/project/SpeechRecognition/)
  - Mediapipe (https://ai.google.dev/edge/mediapipe/solutions/guide?hl=fr)

---

## Project Timeline

### Release 1.0 (25%)
- **Features**:
  - Basic voice commands for drone control
  - Initial photo capture functionality
  - API setup for communication with the web server
  - Basic gallery view in the web application

### Release 2.0 (50%)
- **Features**:
  - Gesture-based flight control
  - Facial recognition system implementation
  - Web application enhancements (facial data display, filtering, and search)
  - Basic drone statistics tracking

### Release 3.0 (75%)
- **Features**:
  - Automatic face tracking and real-time synchronization
  - Advanced statistics visualization
  - Admin dashboard for data management

### Release 4.0 (100%)
- **Features**:
  - Full integration of drone and web application functionalities
  - Performance optimization and scalability
  - Security enhancements (API protection, encryption, access control)
  - Comprehensive testing, documentation, and deployment

---

## Setup and Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- SQL database (MySQL/PostgreSQL)
- Tello DJI drone
- Computer microphone for voice control

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/YourUsername/DroneInteractiveControl.git
   ```
2. Navigate to the project directory:
   ```sh
   cd DroneInteractiveControl
   ```
3. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Install Node.js dependencies:
   ```sh
   npm install
   ```
5. Set up the database by running the SQL script provided in the `db` folder.
6. Configure API keys and environment variables (e.g., drone API access, database credentials) in the `.env` file.
7. Start the back-end server:
   ```sh
   npm run server
   ```
8. Start the front-end application:
   ```sh
   npm run client
   ```

---

## Usage

### Controlling the Drone
- Use voice commands via the connected microphone
- Use predefined gestures for movement control

### Accessing the Web Application
- Navigate to `http://localhost:3000` (or the deployed URL)
- Log in to view and manage drone data

---

## Contribution Guidelines

1. Fork the repository.
2. Create a new feature branch:
   ```sh
   git checkout -b feature/new-feature
   ```
3. Commit your changes:
   ```sh
   git commit -m "Add new feature"
   ```
4. Push the branch to your fork:
   ```sh
   git push origin feature/new-feature
   ```
5. Create a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For questions, suggestions, or issues, please contact:

- **Thomas Fiancette** (Project Lead) - [email@example.com]
- **Charles Fassel-Ashley** - [email@example.com]
- **Eliyan Dochev** - [email@example.com]

