#!/usr/bin/python
#----------------------------------------------------------------------#
# See "docs/License.txt" for License Info
#----------------------------------------------------------------------#

## IMPORTS ##

### PANDA Imports ###
from panda3d.core import Vec4, VBase3
from direct.showbase.DirectObject import DirectObject

## Client Imports ##
from client.core.stateUtil import InputCommands, State, StateUtil

########################################################################
########################################################################

(KEY_FWD,
KEY_BACK,
KEY_LEFT,
KEY_RIGHT) = range(4)

YVEC = VBase3(0, 1, 0)
XVEC = VBase3(1, 0, 0)

### MAIN INPUT CLASS ###

class Input(DirectObject):
    """Handle all client related code"""
    
    def __init__(self, _client):
        self.client = _client

        # Setup key listening
        self.keyMap = {"KEY_FWD":0, "KEY_BACK":0, "KEY_LEFT":0, "KEY_RIGHT":0}
         
        self.accept("w", self.setKey, ['KEY_FWD', 1])
        self.accept("s", self.setKey, ['KEY_BACK', 1])
        self.accept("a", self.setKey, ['KEY_LEFT', 1])
        self.accept("d", self.setKey, ['KEY_RIGHT', 1])
       
        self.accept("w-up", self.setKey, ['KEY_FWD', 0])
        self.accept("s-up", self.setKey, ['KEY_BACK', 0])
        self.accept("a-up", self.setKey, ['KEY_LEFT', 0])
        self.accept("d-up", self.setKey, ['KEY_RIGHT', 0])

    # Returns a list of cmds pressed by the player
    def getCommands(self):
        keys = []

        if (self.keyMap['KEY_FWD']):
            keys.append(KEY_FWD)
           
        elif (self.keyMap['KEY_BACK']):
            keys.append(KEY_BACK)
           
        if (self.keyMap['KEY_RIGHT']):
            keys.append(KEY_RIGHT)
           
        elif (self.keyMap['KEY_LEFT']):
            keys.append(KEY_LEFT)
 
        return keys

    def setKey(self, key, value):
        self.keyMap[key] = value