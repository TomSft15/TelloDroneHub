
class Commands:
    def __init__(self, drone):
        self.drone = drone
        
    def takeoff(drone):
        drone.takeoff()
        
    def land(drone):
        drone.land()
        
    def stop(drone):
        drone.emergency()
    
    def forward(drone):
        rc_control = [0, 50, 0, 0]
        return rc_control

    def backward(drone):
        rc_control = [0, -50, 0, 0]
        return rc_control
        
    def left(drone):
        rc_control = [-50, 0, 0, 0]
        return rc_control

    def right(drone):
        rc_control = [50, 0, 0, 0]
        return rc_control
        
    def up(drone):
        rc_control = [0, 0, 50, 0]
        return rc_control

    def down(drone):
        rc_control = [0, 0, -50, 0]
        return rc_control

    def rotateLeft(drone):
        rc_control = [0, 0, 0, -50]
        return rc_control

    def rotateRight(drone):
        rc_control = [0, 0, 0, 50]
        return rc_control

    def flipLeft(drone):
        drone.flip_left()

    def flipRight(drone):
        drone.flip_right()

    def flipForward(drone):
        drone.flip_forward()

    def flipBackward(drone):
        drone.flip_backward()