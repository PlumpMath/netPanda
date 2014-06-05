#!/usr/bin/python
#----------------------------------------------------------------------#
# See "docs/License.txt" for License Info
#----------------------------------------------------------------------#

# Load config

## IMPORTS ##
import os
import sys
import copy

### PANDA Imports ###
from direct.showbase.DirectObject import DirectObject

## Server Imports ##
from server.stateUtil import StateUtil
from clientPlayer import ClientPlayer

## Client Imports ##

########################################################################
########################################################################


### SERVER STATE CLASS ###

class ServerState():
    
    def __init__(self, _server):
    	self.server = _server
        self.networkMgr = self.server.networkManager
    	# Dict self.clients
    	self.clients = self.server.activeCPlayers
        self.connections = self.server.activeConnections

        # keep hold of the lastClient id that joined the server
        self.lastJoinedClientId = None

    	# Server update time
    	self.tickTime = 1.0 / 20

    	self.delay = 0
    	self.gotCmds = False
    	self.lastTime = 0


    # Server update
    def update(self):
    	nowTime = StateUtil.getTime()
    	# Here goes the input updates per client
    	self.newClientInputTimes(nowTime)

    	self.delay += (nowTime - self.lastTime) / 1000.0
    	self.lastTime = nowTime

        if self.delay > self.tickTime:
            if self.gotCmds:
                self.broadcastUpdates()

            self.delay = 0

    	# Update serverClient State
        self.newClientLocalUpdate()

    # Check if we have newCmds from anyClient
    def gotCommands(self, _clientID, _cmds):
    	self.gotCmds = True
    	self.clients[_clientID].inputCmds = _cmds
    	self.clients[_clientID].inputCmds.oldTime = copy.deepcopy(_cmds.t)


    # Network Broadcast all
    def broadcastUpdates(self):
    	"""Broadcast to all connected clients"""
        for conn in self.connections:
            for client in self.clients:
                clId = self.clients[client].id
                clState = self.clients[client].state
                clInputOldTime = self.clients[client].inputCmds.oldTime
                self.networkMgr.command.broadcastUpdates(clId, clState, clInputOldTime, conn)

    # Broadcast the latest player that joined
    # to the others that are already online
    def broadcastNewClient(self, _id, _state):
        """Broadcast the id and state of the latest client that joined"""
        for conn in self.connections:
            for client in self.clients:
                if client == _id:
                    pass
                else:
                    self.networkMgr.command.broadcastNewClient(_id, _state, conn)


    # Utils
    def newClientInputTimes(self, _nowTime):
    	"""Update the server client input times"""
    	for client in self.clients:
    		self.clients[client].inputCmds.t = _nowTime

    def newClientLocalUpdate(self):
    	"""Update the server client states"""
    	for client in self.clients:
            clState = self.clients[client].state
            clCmds = self.clients[client].inputCmds
            self.clients[client].state = StateUtil.updateState(clState, clCmds)

    # Create a playerObj for a newly joined client
    def newClientPlayerObj(self, _id, _netCon):
        """
        Create a playerObj for a newly joined client.
        _id - "ClientNanem
        _netCon - Client Connection
        """
        self.clients[_id] = ClientPlayer(self, _id, _netCon)


