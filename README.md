# Tello DJI Drone Control Project

## Project Overview

This project consists of a comprehensive application to control a Tello DJI drone through various intuitive user interfaces. The main objective is to offer multiple modes of interaction with the drone, including voice commands, gestures, and facial recognition, all integrated into a user-friendly web interface.

---

## Main Features

### Drone Control
- **Keyboard Control**: Pilot the drone with arrow keys and keyboard shortcuts
- **Voice Commands**: Control the drone through voice recognition (e.g., "take off", "land", "move forward")
- **Gesture Control**: Hand gesture detection to pilot the drone
- **Automatic Facial Tracking**: The drone can detect and follow a face automatically

### User Interface
- **Dashboard**: Real-time visualization of drone telemetry data
- **Video Stream**: Display of the drone's embedded camera video feed
- **Photo Capture**: Ability to take photos from the drone
- **Customization**: Configuration of keyboard controls according to user preferences

### Other Features
- **Facial Recognition**: Detection and identification of people
- **Flight Statistics**: Tracking of flight duration, battery level, etc.
- **Emergency Mode**: Emergency commands to ensure flight safety

---

## Technical Architecture

### Backend (Python)
- **Flask** framework for REST API
- **Flask-RESTx** for automatic API documentation with Swagger
- **OpenCV** for image processing and facial detection
- **Mediapipe** for gesture recognition
- **SpeechRecognition** for voice recognition
- **djitellopy** for interfacing with the Tello drone

### Frontend (Vue.js)
- **Vue.js 3** as the frontend framework
- Modular components for different control modes
- **socket.io** for real-time communication
- Responsive interface accessible on computers and mobile devices

---

## Project Structure

The project is organized into two main parts:

### Backend
- `app.py`: Entry point of the Flask application
- `controllers/`: Controllers for different functionalities (drone, video, gestures, etc.)
- `services/`: Business logic for drone control, video processing, etc.
- `models/`: Data models
- `utils/`: Various utilities

### Frontend
- `src/components/`: Reusable Vue.js components
- `src/views/`: Main application views
- `src/services/`: Services for API and frontend functionalities
- `src/mixins/`: Shared functionalities like keyboard controls

---

## Installation and Usage

### Prerequisites
- Python 3.8+ with pip
- Node.js and yarn
- A Tello DJI drone
- Wi-Fi connection to connect to the drone

### Backend Installation
1. Create a Python virtual environment
2. Install dependencies via `pip install -r requirements.txt`
3. Launch the server with `python app.py`

### Frontend Installation
1. Install dependencies via `yarn install`
2. Launch the development server with `yarn serve`

### Connecting to the Drone
1. Turn on the Tello drone
2. Connect to the drone's Wi-Fi network from your computer
3. Use the "Connect a drone" interface in the application
4. Once connected, access the dashboard to control the drone

---

## Important Technical Features

- RESTful API documented with Swagger UI
- Modular architecture for easy extension
- Implementation of different control types (keyboard, voice, gesture)
- Simulation mode allowing use of the application without a drone
- Responsive design for different screen sizes

---

## Troubleshooting Common Issues

1. **The drone doesn't connect**:
   - Check that you are properly connected to the drone's Wi-Fi network
   - Make sure the drone's battery is sufficiently charged
   - Restart the drone and the application

2. **Voice recognition doesn't work**:
   - Check that your browser supports the Web Speech API (Chrome recommended)
   - Make sure your microphone is correctly configured and authorized

3. **Gesture detection is not accurate**:
   - Make sure you are in a well-lit environment
   - Position yourself about 1 meter from the camera
   - Make clear and distinct gestures

4. **"Port already in use" error**:
   - Make sure no other program is using ports 5000 (backend) or 8080 (frontend)
   - Restart your computer to free up the ports

---

## Future Development

- Addition of mapping features and GPS navigation
- Improvement of facial recognition algorithms
- Support for multiple drones simultaneously
- Automated programmed mission mode
- Export of flight data and integration with other applications

This project represents a complete interface between humans and drones, offering multiple interaction modalities adapted to different use cases, from recreational use to more professional applications.

---

## Licence

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

### What this license means:

- You are free to use, modify, and distribute this software.
- If you modify the software, you must distribute those modifications under the same license.
- If you use this software in a web application or network service, you must make the complete source code available to users of that service.
- This license protects against the appropriation of code in closed products, including web services.

See the `LICENSE.md` file for the full license text.

---

## Contact

For any questions, suggestions, or issues, please contact:

- **Thomas Fiancette** (Project Lead) - [thomas.fiancette@epitech.eu]
- **Charles Fassel-Ashley** - [charles.fassel-ashley@epitech.eu]
- **Eliyan Dochev** - [eliyan.dochev@epitech.eu]

---

## Acknowledgements

- DJI development team for the Tello SDK
- Contributors to OpenCV, Mediapipe, and other open-source tools used in this project