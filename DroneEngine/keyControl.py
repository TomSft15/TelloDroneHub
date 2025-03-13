from getKeyPressed import getKeyPressed
from speechRecognitionModule import speechToText

def executeVoiceCommand(command, commandsClass):
    rc_control = [0, 0, 0, 0]
    if "take off" in command:
        commandsClass.takeoff()
    elif "land" in command:
        commandsClass.land()
    
    if "forward" in command:
        rc_control = commandsClass.forward()
    elif "backward" in command:
        rc_control = commandsClass.backward()
    
    if "left" in command:
        rc_control = commandsClass.left()
    elif "right" in command:
        rc_control = commandsClass.right()
    
    if "up" in command:
        rc_control = commandsClass.up()
    elif "down" in command:
        rc_control = commandsClass.down()
    
    if "rotate left" in command:
        rc_control = commandsClass.rotateLeft()
    elif "rotate right" in command:
        rc_control = commandsClass.rotateRight()
    
    if "flip left" in command:
        commandsClass.flipLeft()
    elif "flip right" in command:
        commandsClass.flipRight()
    
    if "flip forward" in command:
        commandsClass.flipForward()
    elif "flip backward" in command:
        commandsClass.flipBackward()
    
    if "stop" in command:
        commandsClass.stop()
    
    return rc_control

def key_control(drone, commandsClass=None):
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
    
    if getKeyPressed("h"): drone.flip_right()
    elif getKeyPressed("f"): drone.flip_left()
    
    if getKeyPressed("i"):
        command = speechToText()
        if command:
            [lr, fb, ud, xy] = executeVoiceCommand(command, commandsClass)
 
    if getKeyPressed("e"): drone.land()
    
    if getKeyPressed("m"):
        drone.land()
        drone.end()
        quit()

    if getKeyPressed("p"):
        drone.emergency()
        
    return [lr, fb, ud, xy]