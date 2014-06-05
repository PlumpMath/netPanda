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

## Client Imports ##
from opcodes import *
from stateUtil import State, InputCommands


########################################################################
########################################################################

# Client Commands
class Command():
    
    def __init__(self, _networkManager):
    	self.networkMgr = _networkManager
        self.client = self.networkMgr.client

        # Local TCP Connection
        self.tcpCon = None

        # Local Player info
        self.localId = self.networkMgr.client.id

    def authREQ(self, _tcpCon):
        """
        Handle the login packet to server.
        """
        # Reset the TcpConnection
        self.tcpCon = _tcpCon
        # Create the buffer
        pkg = PyDatagram()
        
        # Add the opcode
        pkg.addUint16(cmdToServer_doAuth)
        
        pkg.addString(self.localId)
        
        # Send the packet
        self.networkMgr.tcpWriter.send(pkg, _tcpCon)
        
    def authResponse(self, opcode, data):
        """
        Handle the smsg regarding Auth between client and server
        Note: This is really simple.
        """

        # Ack msg
        returnId = data.getString()
        print "Client: Returned ID -", returnId

        # State.pos
        currentServerStatePos = data.getString()
        # State.t
        currentServerStateTime = data.getString()

        statePos = eval(currentServerStatePos)
        stateTime = eval(currentServerStateTime)

        newState = State()
        newState.pos = statePos
        newState.t = stateTime

        # Check if its a local player
        if returnId == self.localId:
            # Create the local player object
            self.client.clientState.newPlayerObject(returnId, newState, True)
            self.client.clientState.setLocalClient()
        else:
            # Create the local player object
            self.client.clientState.newPlayerObject(returnId, newState, False)

    # Handle a new player that joined
    def newPlayerJoined(self, opcode, data):
        """Create a new player that joined on a active server"""

        clId = data.getString()
        clStateP = data.getString()
        clStatePos = eval(clStateP)
        clStateT = data.getString()
        clStateTime = eval(clStateT)

        newPlayerState = State()
        newPlayerState.pos = clStatePos
        newPlayerState.t = clStateTime

        # Create the player: hope that his not already created #_#
        self.client.clientState.newPlayerObject(clId, newPlayerState, False)

    def sendCommands(self, inputCmds):
    	"""Send movement commands to the server"""
    	pkg = PyDatagram()
    	pkg.addUint16(cmdToServer_moveCmds)

        cmds = inputCmds.cmds
        t = inputCmds.t
    	# Convert movement list to string for now... 
    	# eval on serverside
    	toStr = str(cmds)
        pkg.addString(self.localId)
    	pkg.addString(toStr)
        pkg.addUint64(t)

    	# Send the packet
    	self.networkMgr.tcpWriter.send(pkg, self.tcpCon)

    def updateState(self, opcode, data):
        """Gets the new states from the server"""

        # Get id
        clId = data.getString()
        # get State.pos
        clStateP = data.getString()
        clStatePos = eval(clStateP)
        # get state.t
        clStateTime = data.getUint64()
        # get inputTime.oldTime
        clInputOldT = data.getString()
        clInputOldTime = eval(clInputOldT)

        newPlayerState = State()
        newPlayerState.pos = clStatePos
        newPlayerState.t = clStateTime

        newPlayerInput = InputCommands()
        newPlayerInput.oldTime = clInputOldTime

        self.client.clientState.getServerState(clId, newPlayerState, newPlayerInput)
