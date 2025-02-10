import pygame as py

def init_pygame():
    py.init()
    py.display.set_mode((360, 240))
    
def getKeyPressed(key):
    stat = False
    for eve in py.event.get(): pass
    keyInput = py.key.get_pressed()
    myKey = getattr(py, 'K_{}'.format(key))
    if keyInput[myKey]:
        stat = True
    py.display.update()
    return stat