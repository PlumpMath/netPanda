#!/usr/bin/python
#----------------------------------------------------------------------#
# See "docs/License.txt" for License Info
#----------------------------------------------------------------------#

# Load config

## IMPORTS ##
import time
import copy

### PANDA Imports ###
from panda3d.core import Vec4, VBase3

## Client Imports ##

########################################################################
########################################################################

(KEY_FWD,
KEY_BACK,
KEY_LEFT,
KEY_RIGHT) = range(4)
 
YVEC = VBase3(0, 1, 0)
XVEC = VBase3(1, 0, 0)

### SERVER STATEUTIL CLASS ###

# Main state updater
class StateUtil():
    
    # Method used for updating the player movements
    # Exactly the same on both server and client
    @staticmethod
    def updateState(_state, _inputCmds):
    	dt = (_inputCmds.t - _state.t) / 1000.0
    	cmds = _inputCmds.cmds

    	moveVec = VBase3(0, 0, 0)
        
        if KEY_FWD in cmds:
            moveVec += YVEC
        elif KEY_BACK in cmds:
            moveVec -= YVEC
        if KEY_RIGHT in cmds:
            moveVec += XVEC
        elif KEY_LEFT in cmds:
            moveVec -= XVEC
           
        moveVec.normalize()
        newPos = _state.pos + moveVec * 2 * dt
       
        return State(newPos, _inputCmds.t + 0.0)

    # Get the time 
    @staticmethod
    def getTime():
    	return int(round(time.time() * 1000))

# State class
class State():
	"""
	This is used to create states for the players
	pos = position of the player
	t = timestamp for this state
	"""
	def __init__(self, _pos=VBase3(0, 0, 0), _t=0):
		self.pos = _pos
		self.t = _t

# InputCommands Class Holder for each player
class InputCommands():
	"""
	Cmds = List of keyboard input Cmds
	t = client to server timestamp and then server to client
	oldTime = Holds the last timestamp from the client, gets updated
	  			on each new Tick
	"""
	def __init__(self, _cmds=[], _t=0):
		self.cmds = _cmds
		self.t = _t
		self.oldTime = 0

# Snapshot class holds state and cmds last used
class Snapshot():
	"""
	inputCmds = InputCommands obj for a client
	state = State obj for a client
	"""
	def __init__(self, _inputCmds, _state):
		self.inputCmds = _inputCmds
		self.state = _state

