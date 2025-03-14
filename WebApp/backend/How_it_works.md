# How It Works

## System Architecture Overview

Our system consists of three main components:
1. **Tello Drone**: The physical drone with camera
2. **Flask API Server**: Our backend running the face recognition
3. **Client Application**: Web/mobile app that interfaces with the API

## Connection and Data Flow

Here's how data flows through the system:

```
[Tello Drone] <---> [Flask API Server] <---> [Client Application]
   (UDP)                (REST API)            (HTTP Requests)
```

## Server-Drone Connection

The server connects to the drone using these mechanisms:

1. **Control Connection**: UDP on port 8889 (defined in config.py)
2. **Video Stream**: The drone streams video which our server captures and processes
3. **State Information**: The drone sends telemetry data (battery, height, etc.)

## Complete Workflow

### 1. Server Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

The server starts on port 5000 with all endpoints ready, but not yet connected to any drone.

### 2. Client Connection Sequence

A client application would follow these steps:

#### Step 1: Connect to Drone

```
GET /drone/connect
```

This endpoint:
- Checks if port 8889 is available
- Initializes the Tello drone object
- Establishes a connection
- Starts a background thread to update drone data
- Automatically starts video streaming

Response:
```json
{
  "success": true,
  "message": "Drone connected successfully"
}
```

#### Step 2: Verify Connection

```
GET /status
```

Response:
```json
{
  "connected": true,
  "drone_data": {
    "battery": 87,
    "temperature": 32,
    "flight_time": 0,
    "height": 0,
    "speed": 0,
    "signal": 100
  }
}
```

#### Step 3: Upload Reference Faces

The client must upload photos of people to recognize:

```
POST /face/upload
Content-Type: multipart/form-data

file: [image file]
name: "John Doe"
```

Response:
```json
{
  "success": true,
  "message": "Face uploaded for John Doe"
}
```

#### Step 4: List Known Faces

```
GET /face/list
```

Response:
```json
{
  "faces": ["john_doe", "jane_smith"]
}
```

#### Step 5: Start Face Recognition

```
GET /face/start
```

This endpoint:
- Initializes the face recognition system
- Starts the frame collector thread (captures frames at intervals)
- Starts the face recognizer thread (processes frames from queue)

Response:
```json
{
  "success": true,
  "message": "Face recognition started"
}
```

#### Step 6: Enable Face Overlay

```
GET /video/faces/show
```

This enables showing recognition boxes and names on the video feed.

Response:
```json
{
  "success": true,
  "message": "Face recognition overlay enabled"
}
```

#### Step 7: Access Video Feed

The client can now display the video stream with face recognition:

```
GET /video/feed
```

This returns an MJPEG stream that browsers can display in an `<img>` tag:

```html
<img src="http://server-address:5000/video/feed" />
```

#### Step 8: Monitor Recognition Results

Get the latest recognition results programmatically:

```
GET /face/current
```

Response:
```json
{
  "recognitions": [
    {
      "name": "John Doe",
      "position": [120, 80, 100, 100]
    }
  ],
  "timestamp": 1615493385.7291
}
```

#### Step 9: Monitor System Health

```
GET /health
```

Response:
```json
{
  "cpu_usage": 23.5,
  "memory_usage": 128.7,
  "video_fps": 25.3,
  "thread_count": 8,
  "threads": [
    {"name": "MainThread", "is_alive": true},
    {"name": "VideoCaptureThread", "is_alive": true},
    {"name": "FrameCollector", "is_alive": true},
    {"name": "FaceRecognizer", "is_alive": true}
  ],
  "timestamp": 1615493385.7291
}
```

#### Step 10: Control the Drone (Optional)

```
GET /drone/takeoff  # Take off
GET /drone/land     # Land
```

#### Step 11: Shutdown Sequence

When finished:

```
GET /face/stop      # Stop face recognition
GET /video/stop     # Stop video streaming
GET /drone/land     # Land the drone (if flying)
GET /drone/disconnect  # Disconnect from drone
```

## Behind the Scenes: How Face Recognition Works

1. **Frame Collection**:
   - The `FrameCollector` thread captures frames from the video stream
   - Only processes every Nth frame (defined by `FACE_RECOGNITION_INTERVAL`)
   - Places frames in a bounded queue (sized by `MAX_QUEUE_SIZE`)

2. **Face Recognition**:
   - The `FaceRecognizer` thread takes frames from the queue
   - Detects faces using OpenCV's Haar Cascade classifier
   - Calculates face encodings by resizing, converting to grayscale, and flattening
   - Compares against known faces using Euclidean distance
   - Updates the `current_recognitions` list with results

3. **Video Rendering**:
   - The `VideoService` takes the raw video frame
   - If face overlay is enabled, it draws rectangles and names based on recognition results
   - Adds FPS information
   - Streams the processed frames as MJPEG
