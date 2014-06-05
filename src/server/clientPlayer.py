#!/usr/bin/python
#----------------------------------------------------------------------#
# See "docs/License.txt" for License Info
#----------------------------------------------------------------------#

# Load config

## IMPORTS ##

### PANDA Imports ###

## Server Imports ##
from server.stateUtil import StateUtil, State, InputCommands

########################################################################
########################################################################


### SERVER CLIENT PLAYER CLASS ###

class ClientPlayer():
    
    def __init__(self, _server, _id, _netCon):
    	self.server = _server

    	# player details
    	self.id = _id
    	self.state = State()
    	self.inputCmds = InputCommands()
    	self.inputCmds.oldTime = float('+infinity')
    	self.netConnection = _netCon

        # Debug TEMP
        print "Server: New Player ", self.id

    def update(self):
    	pass
