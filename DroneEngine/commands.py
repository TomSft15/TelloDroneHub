class Commands:
    def __init__(self, drone):
        self.drone = drone
        
    def takeoff(self):
        self.drone.takeoff()
        
    def land(self):
        self.drone.land()
        
    def stop(self):
        self.drone.emergency()
    
    def forward(self):
        return [0, 50, 0, 0]

    def backward(self):
        return [0, -50, 0, 0]
        
    def left(self):
        return [-50, 0, 0, 0]

    def right(self):
        return [50, 0, 0, 0]
        
    def up(self):
        return [0, 0, 50, 0]

    def down(self):
        return [0, 0, -50, 0]

    def rotateLeft(self):
        return [0, 0, 0, -50]

    def rotateRight(self):
        return [0, 0, 0, 50]

    def flipLeft(self):
        self.drone.flip_left()

    def flipRight(self):
        self.drone.flip_right()

    def flipForward(self):
        self.drone.flip_forward()

    def flipBackward(self):
        self.drone.flip_backward()
