#!/usr/bin/python
#----------------------------------------------------------------------#
# See "docs/License.txt" for License Info
#----------------------------------------------------------------------#

## IMPORTS ##
import os
import sys

### PANDA Imports ###
from pandac.PandaModules import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

## Server Imports ##
from opcodes import *
from stateUtil import InputCommands, State
## Client Imports ##

########################################################################
########################################################################

class Command():
    
    def __init__(self, _networkManager):
    	self.networkMgr = _networkManager
        self.server = self.networkMgr.server
        self.connections = self.server.activeConnections
        self.clients = self.server.activeCPlayers

    def doAuth(self, opcode, data, _client):
        """
        Handle auth for a single client connecting
        """
        
        ## Get the client id 
        newClientId = data.getString()
        print "Server: New client connected -", newClientId
        self.server.serverState.lastJoinedClientId = newClientId

        # Create the player into the server players holder
        self.server.serverState.newClientPlayerObj(newClientId, _client)
        

        # Get all connected clientPlayers states and ids
        #for conn in self.connections:
        for client in self.clients:
            clId = self.clients[client].id
            clState = self.clients[client].state
            # Create buffer
            pkg = PyDatagram()
        
            # Add response
            pkg.addUint16(cmdToClient_authResponse)
            pkg.addString(clId)
            pkg.addString(str(clState.pos))
            pkg.addString(str(clState.t))
        
            self.networkMgr.tcpWriter.send(pkg, _client)
            # maybe add a if to check to update other players about the new guy

        # tell other connected players about the new player
        newClientState = self.clients[newClientId].state
        self.server.serverState.broadcastNewClient(newClientId, newClientState)


    def moveCmds(self, opcode, data, client):
        """Get new moveCmds from the client"""

        clId = data.getString()
        cmdsStr = data.getString()
        cmds = eval(cmdsStr)
        clTimeStamp = data.getUint64()

        newClCmds = InputCommands()
        newClCmds.cmds = cmds
        newClCmds.t = clTimeStamp

        self.server.serverState.gotCommands(clId, newClCmds)


    # Send player State
    def broadcastUpdates(self, _clId, _clState, _clInputOldTime, _conn):
        """Send the serverState to the client"""

        pkg = PyDatagram()
        pkg.addUint16(cmdToClient_newState)

        # Actual packet data
        pkg.addString(_clId)
        pkg.addString(str(_clState.pos))
        pkg.addUint64(_clState.t)
        pkg.addString(str(_clInputOldTime))

        self.networkMgr.tcpWriter.send(pkg, _conn)

    # Broadcast to all other players about the new player that joined
    def broadcastNewClient(self, _id, _state, _conn):

        pkg = PyDatagram()

        pkg.addUint16(cmdToClient_newPlayerJoined)
        pkg.addString(_id)
        pkg.addString(str(_state.pos))
        pkg.addString(str(_state.t))

        self.networkMgr.tcpWriter.send(pkg, _conn)
