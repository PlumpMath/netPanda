#!/usr/bin/python
#----------------------------------------------------------------------#
# See "docs/License.txt" for License Info
#----------------------------------------------------------------------#

# Load config

## IMPORTS ##
import os
import sys

### PANDA Imports ###
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task

## Client Imports ##
from client.core.networkManager import NetworkManager
from client.core.clientState import ClientState
from client.camera.camera import BasicCamera
from client.input.input import Input

########################################################################
########################################################################


### MAIN CLIENT CLASS ###

class Client(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)

        self.isDebugOn = True
        
        if self.isDebugOn:
            print "Client: Debug - ON"
            
        ## HOLDERS ##
        self.id = "TestClient1"
        self.hasLocalPlayer = False
        self.isConnected = False
        self.tcpConnection = None
        self.localPlayer = {}
        self.otherPlayers = {}

        # Start network manager
        self.networkManager = NetworkManager(self)
        # Connect to a server with the given ip
        self.networkManager.connectToServer('127.0.0.1')
        # Start Client state
        self.clientState = ClientState(self)

        # Start the update tasks
        t = taskMgr.add(self.update, 'update')
        t.last = 0

        ### SETUP OTHER CLIENT PARTS ###
        self.mainCamera = BasicCamera(self)
        self.input = Input(self)


    # Start Update
    def update(self, task):
        """
        Start the gamestate update task
        """
        if self.hasLocalPlayer:
            self.clientState.update()
        return task.cont
        



client = Client()
run()