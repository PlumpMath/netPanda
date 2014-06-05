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

## Server Imports ##
from server.networkManager import NetworkManager
from server.serverState import ServerState
## Client Imports ##

########################################################################
########################################################################


### MAIN GAMESERVER CLASS ###

class Server(ShowBase):
    
    def __init__(self):

        self.isDebugOn = False
        
        if self.isDebugOn:
            ShowBase.__init__(self)
        else:
            # Start showbase(panda)
            ShowBase(windowType = 'none')
        

        ## CLIENT HOLDERS ##
        self.activeConnections = []
        self.activeCPlayers = {}

        # Start network manager
        self.networkManager = NetworkManager(self)
        # Start Server Game State
        self.serverState = ServerState(self)

        # Start the update tasks
        t = taskMgr.add(self.update, 'update')
        t.last = 0

        # Prints wtf ever
        print "Server: Active!"
        print "Waiting for connections...."

    # Start Update
    def update(self, task):
        """
        Start the gamestate update task
        """
        self.serverState.update()
        return task.cont
        



server = Server()
run()