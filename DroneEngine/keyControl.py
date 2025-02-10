from getKeyPressed import getKeyPressed

def key_control(drone):
    lr, fb, ud, xy = 0, 0, 0, 0
    x = 50
    
    if getKeyPressed("a"): drone.takeoff()
    
    if getKeyPressed("q"): lr = -x
    elif getKeyPressed("d"): lr = x
    
    if getKeyPressed("z"): fb = x
    elif getKeyPressed("s"): fb = -x
    
    if getKeyPressed("UP"): ud = x
    elif getKeyPressed("DOWN"): ud = -x
    
    if getKeyPressed("LEFT"): xy = -x
    elif getKeyPressed("RIGHT"): xy = x
    
    if getKeyPressed("e"): drone.land()
    
    if getKeyPressed("m"):
        drone.land()
        drone.end()
        quit()

    if getKeyPressed("p"):
        drone.emergency()
        
    return [lr, fb, ud, xy]