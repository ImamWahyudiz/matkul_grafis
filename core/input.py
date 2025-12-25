import pygame
from pygame import key


class Input(object):
    def __init__(self):
        #has the user quit the application
        self.quit = False
        #lists to store key states
        #down, up: discrete event. lasts for one iteration
        #pressed: continous event, between down and up events
        self.keyDownList = []
        self.keyPressedList = []
        self.keyUpList = []
        
        #mouse states
        self.mouseButtonDownList = []
        self.mouseButtonPressedList = []
        self.mouseButtonUpList = []
        self.mousePosition = (0, 0)
        self.mouseDelta = (0, 0)
        self.lastMousePosition = (0, 0)

    def update(self):
        #reset discrete key states
        self.keyDownList = []
        self.keyUpList = []
        
        #reset discrete mouse states
        self.mouseButtonDownList = []
        self.mouseButtonUpList = []
        
        #update mouse position and delta
        currentMousePosition = pygame.mouse.get_pos()
        self.mouseDelta = (
            currentMousePosition[0] - self.lastMousePosition[0],
            currentMousePosition[1] - self.lastMousePosition[1]
        )
        self.lastMousePosition = currentMousePosition
        self.mousePosition = currentMousePosition

        #iterative over all user input events such as keyboard or mouse 
        #since the last time events were checked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            #check for keydown and keyup events
            #get name of key from event
            #and append to or remove from correspoding lists
            if event.type == pygame.KEYDOWN:
                keyName = pygame.key.name(event.key)
                self.keyDownList.append(keyName)
                self.keyPressedList.append(keyName)
            if event.type == pygame.KEYUP:
                keyName = pygame.key.name(event.key)
                self.keyPressedList.remove(keyName)
                self.keyUpList.append(keyName)
            
            #mouse button events
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseButtonDownList.append(event.button)
                if event.button not in self.mouseButtonPressedList:
                    self.mouseButtonPressedList.append(event.button)
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouseButtonUpList.append(event.button)
                if event.button in self.mouseButtonPressedList:
                    self.mouseButtonPressedList.remove(event.button)

    #functions to check key states
    def isKeyDown(self, keyCode):
        return keyCode in self.keyDownList
    
    def isKeyPressed(self, keyCode):
        return keyCode in self.keyPressedList
    
    def isKeyUp(self, keyCode):
        return keyCode in self.keyUpList
    
    #functions to check mouse states
    def mouseButtonDown(self, buttonNumber):
        return buttonNumber in self.mouseButtonDownList
    
    def mouseButtonPressed(self, buttonNumber):
        return buttonNumber in self.mouseButtonPressedList
    
    def mouseButtonUp(self, buttonNumber):
        return buttonNumber in self.mouseButtonUpList
    
    def getMousePosition(self):
        return self.mousePosition
    
    def getMouseDelta(self):
        return self.mouseDelta
