#!/usr/bin/python
#----------------------------------------------------------------------#
# See "docs/License.txt" for License Info
#----------------------------------------------------------------------#

## IMPORTS ##
import os
import sys

### PANDA Imports ###
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task.Task import Task

## Client Imports ##
from config import *
from commands import Command
from opcodes import *


########################################################################
########################################################################


### CLIENT NETWORK MANAGER CLASS ###

class NetworkManager():
    
    def __init__(self, _client):
    	self.client = _client

        # Tcp Connection
        self.tcpCon = None

    	# Start TCP
    	self.startTcp()
    	#self.startUdp()

    	# Start network tasks for readers
        # TCP Reader
        taskMgr.add(self.tcpReaderTask, "tcpReaderTask", -39)
        # UDP Reader
        #taskMgr.add(self.udpReaderTask, "udpReaderTask", -39)
        print "Client: Readers Started!"

        # Create Commands
        self.command = Command(self)
        self.commands = {
            cmdToClient_authResponse   : self.command.authResponse,
            cmdToClient_newState       : self.command.updateState,
            cmdToClient_newPlayerJoined: self.command.newPlayerJoined
        }

    ## SETUP TCP ##
    def startTcp(self):
    	"""
    	Setup all tcp related classes
    	"""
        self.tcpManager = QueuedConnectionManager()
        self.tcpReader = QueuedConnectionReader(self.tcpManager, 0)
        self.tcpWriter = ConnectionWriter(self.tcpManager, 0)

    def startUdp(self):
    	"""
    	Setup all udp related classes
    	"""
        self.udpManager = QueuedConnectionManager()
        self.udpReader = QueuedConnectionReader(self.udpManager, 0)
        self.udpWriter = ConnectionWriter(self.udpManager, 0)

    # TCP Reader Task
    def tcpReaderTask(self, task):
        """
        Handle any data from server by sending it to the Handlers.
        """
        while 1:
            (datagram, data, opcode) = self.tcpNonBlockingRead(self.tcpReader)
            if opcode is MSG_NONE:
                # Do nothing or use it as some 'keep_alive' thing.
                break 
            else:
                # Handle it
                self.tcpHandleDatagram(data, opcode)
                
        return Task.cont

    # TCP NonBlockingRead
    def tcpNonBlockingRead(self, qcr):
        """
        Return a datagram collection and type if data is available on
        the queued connection tcpReader
        
        @param qcr: self.tcpReader
        """
        if self.tcpReader.dataAvailable():
            datagram = NetDatagram()
            if self.tcpReader.getData(datagram):
                data = PyDatagramIterator(datagram)
                opcode = data.getUint16()
                
            else:
                data = None
                opcode = MSG_NONE
            
        else:
            datagram = None
            data = None
            opcode = MSG_NONE
            
        # Return the datagram to keep a handle on the data
        return (datagram, data, opcode)

    # TCP Handle Datagram
    def tcpHandleDatagram(self, data, opcode):
        """
        Check for the handle assigned to the opcode.
        """
        if opcode in self.commands:
        	self.commands[opcode](opcode, data)

        else:
            print "Client: BAD-opcode - %d" % opcode
            print "Client: Opcode Data -", data
            
        return



    # Connect to a Server
    def connectToServer(self, _hostIP):
        # TCP Connection
        self.tcpConnection = self.tcpManager.openTCPClientConnection(_hostIP, 
                                    clTCPPORT, clTIMEOUT)

        if self.tcpConnection != None:
            self.tcpReader.addConnection(self.tcpConnection)
            print "Client: Connected to %s" % _hostIP
            self.tcpCon = self.tcpConnection
            # Temp test
            self.command.authREQ(self.tcpCon)

