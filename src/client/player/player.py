#!/usr/bin/python
#----------------------------------------------------------------------#
# See "docs/License.txt" for License Info
#----------------------------------------------------------------------#

# Load config

## IMPORTS ##

### PANDA Imports ###
from panda3d.core import Vec4
## Client Imports ##
from client.core.stateUtil import StateUtil, State, InputCommands

########################################################################
########################################################################


### GENERAL PLAYER CLASS ###

class Player():
    
    def __init__(self, _client, _id, _state, _isNoneLocal=False):
    	self.client = _client

    	# player details
    	self.id = _id
    	self.state = State()
    	self.inputCmds = InputCommands()
    	self.inputCmds.oldTime = float(0.0)#'+infinity')
        self.isLocal = False

        # new Updates
        if not self.isLocal:
            self.state = _state

        # Load a model
        self.loadModel("client/player/models/pawn")

    def update(self, _state, _inputCmds):
    	self.state = _state
        self.inputCmds = _inputCmds

    def loadModel(self, _modelFile):
        """Load a model file for the given player"""
        self.model = loader.loadModel(_modelFile)
        self.model.setColor(Vec4(0, 1, 0, 1))
        self.model.reparentTo(render) 
