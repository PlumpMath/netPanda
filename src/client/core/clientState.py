#!/usr/bin/python
#----------------------------------------------------------------------#
# See "docs/License.txt" for License Info
#----------------------------------------------------------------------#

## IMPORTS ##
import os
import sys
import copy

### PANDA Imports ###
#from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec4, VBase3

## Client Imports ##
from stateUtil import StateUtil
from client.player.player import Player

########################################################################
########################################################################

### MAIN CLIENT STATE CLASS ###

class ClientState(DirectObject):
    """Handle all client related code"""
    
    def __init__(self, _client):
    	"""Controls Tick update Task, holds state vars"""
        self.client = _client
        self.networkMgr = self.client.networkManager

        # localPlayer holder *Dict
        self.localPlayerDict = self.client.localPlayer

        # otherPlayers *Dict
        self.otherPlayers = self.client.otherPlayers
        self.hasOtherPlayers = False

        ## GAME STATE HOLDERS ##
        self.delay = 0
        self.historicalCmds = []
        self.lastTime = 0

        # Client send/tick time
        self.clientTick = 1.0 / 33

    def setLocalClient(self):
        self.id = self.client.id
        self.localPlayer = self.client.localPlayer[self.id]
        self.localInputCmds = self.localPlayer.inputCmds
        self.localState = self.localPlayer.state

        # Set that we have a local player if info received from server
        self.client.hasLocalPlayer = True

    # Client Main Update task
    def update(self):
    	"""Update"""
    	nowTime = StateUtil.getTime()
        self.newClientUpdateTimes(nowTime)
        self.delay += (nowTime - self.lastTime) / 1000.0
        self.lastTime = nowTime

        # grrr... Shpongle
        if self.delay > self.clientTick:
            # SHould i send the myOther players states to the server?

            self.localInputCmds.cmds = self.client.input.getCommands()
            self.historicalCmds.append(copy.deepcopy((self.localInputCmds, self.localState)))
            
            # Send off the new commands to the server.
            self.networkMgr.command.sendCommands(self.localInputCmds)
            self.delay = 0

        self.localState = StateUtil.updateState(self.localState, self.localInputCmds)

        # Update the player model
        self.updateLocalModel(self.localState)


    # Update local and other player inputCmds time
    def newClientUpdateTimes(self, _nowTime):
    	"""Update the local player and other player's input.t"""
    	self.localInputCmds.t = _nowTime

    	if self.hasOtherPlayers:
    		for otherPlayer in self.otherPlayers:
    			self.otherPlayers[otherPlayer].inputCmds.t = _nowTime


    # Update the local player model and whatever else
    def updateLocalModel(self, _localState):
        """
        Update the local player model and animations. Depending on
        a state check i guess.."""

        self.localPlayer.model.setPos(_localState.pos)

    def updateOtherModels(self, _state):
        """Update the other player's states"""
        for otherPlayer in self.otherPlayers:
            self.otherPlayers[otherPlayer].model.setPos(_state.pos)


    # Get the newStates from the server
    def getServerState(self, _id, _svrState, _clInput):
        """Gets a new updated state from the server"""
        # Update other player's state.pos
        if _id == self.id:
            self.verifyPrediction(_svrState, _clInput)
        else:
            self.updateOtherModels(_svrState)
        
        
    # Compare the old local cmds with the new server updated state
    def verifyPrediction(self, _scrState, _clInput):
        """Update the local player if any faults found since the
        server has main Auth over everything"""
        # remove the old cmds
        while len(self.historicalCmds) > 0 and self.historicalCmds[0][0].t < _clInput:
            self.historicalCmds.pop(0)
       
        if self.historicalCmds:
            diff =  (_svrState.pos - self.historicalCmds[0][1].pos).length()
            print diff
           
            # Recalculate position
            if(diff > 0.2):
                for oldState in self.historicalCmds:
                    serverState = SharedCode.updateState(_svrState, oldState[0])
               
                self.ApplyState(serverState)
                self.localState.pos = serverState.pos


    # Create a new Player Object
    def newPlayerObject(self, _id, _state, _isLocal):
        """Used for creating a LocalPlayer obj and Other player obj's"""
        if _isLocal:
            self.localPlayerDict[_id] = Player(self, _id, _state, _isLocal)
        else:
            self.otherPlayers[_id] = Player(self, _id, _state, _isLocal)


        
















