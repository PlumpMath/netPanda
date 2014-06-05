#!/usr/bin/python
#----------------------------------------------------------------------#
# See "docs/License.txt" for License Info
#----------------------------------------------------------------------#

# Load config

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


### SERVER NETWORK MANAGER CLASS ###

class NetworkManager():
    
    def __init__(self, _server):
    	self.server = _server

    	# Start TCP
    	self.startTcp()
    	#self.startUdp()

    	# Start network tasks for listeners and readers
    	# TCP Listener
        taskMgr.add(self.tcpListenerTask, "tcpListenerTask", -40)
        # TCP Reader
        taskMgr.add(self.tcpReaderTask, "tcpReaderTask", -39)
        # UDP Reader
        #taskMgr.add(self.udpReaderTask, "udpReaderTask", -39)
        print "Server: Listener & Readers Started!"

        # Create Commands
        self.command = Command(self)
        self.commands = {
            cmdToServer_doAuth   : self.command.doAuth,
            cmdToServer_moveCmds : self.command.moveCmds
        }


    ## SETUP TCP ##
    def startTcp(self):
    	"""
    	Setup all tcp related classes
    	"""
        self.tcpManager = QueuedConnectionManager()
        self.tcpReader = QueuedConnectionReader(self.tcpManager, 0)
        self.tcpWriter = ConnectionWriter(self.tcpManager, 0)
        self.tcpListener = QueuedConnectionListener(self.tcpManager, 0)

        # TCP Socket
        self.tcpSocket = self.tcpManager.openTCPServerRendezvous(svrTCPPORT,
                                                    svrBACKLOG)
        self.tcpListener.addConnection(self.tcpSocket)

    def startUdp(self):
    	"""
    	Setup all udp related classes
    	"""
        self.udpManager = QueuedConnectionManager()
        self.udpReader = QueuedConnectionReader(self.udpManager, 0)
        self.udpWriter = ConnectionWriter(self.udpManager, 0)

    # TCP Listener Task
    def tcpListenerTask(self, task):
        """
        Accept new incoming connection from clients, related to TCP
        """
        # Handle new connection
        if self.tcpListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
            
            if self.tcpListener.getNewConnection(rendezvous, netAddress, newConnection):
                newConnection = newConnection.p()
                
                # Tell the reader about the new TCP connection
                self.tcpReader.addConnection(newConnection)
                self.server.activeConnections.append(newConnection)
                    
                print "Server: New Connection from -", str(netAddress.getIpString())
            else:
                print "Server: Connection Failed from -", str(netAddress.getIpString())    
                    
            
        return Task.cont



    # TCP Reader Task
    def tcpReaderTask(self, task):
        """
        Handle any data from clients by sending it to the Handlers.
        """
        while 1:
            (datagram, data, opcode) = self.tcpNonBlockingRead(self.tcpReader)
            if opcode is MSG_NONE:
                # Do nothing or use it as some 'keep_alive' thing.
                break 
            else:
                # Handle it
                self.tcpHandleDatagram(data, opcode, datagram.getConnection())
                
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
    def tcpHandleDatagram(self, data, opcode, client):
        """
        Check for the handle assigned to the opcode.
        """
        if opcode in self.commands:
        	self.commands[opcode](opcode, data, client)
            #messenger.send(opcode, [opcode, data, client])

        else:
            print "Server: BAD-opcode - %d" % opcode
            print "Server: Opcode Data -", data
            
        return