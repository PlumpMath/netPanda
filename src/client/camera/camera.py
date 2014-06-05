#!/usr/bin/python
#----------------------------------------------------------------------#
# See "docs/License.txt" for License Info
#----------------------------------------------------------------------#

## IMPORTS ##

### PANDA Imports ###

## Client Imports ##

########################################################################
########################################################################

class BasicCamera():
    """Hold the MainType camera"""

    def __init__(self, _client):
    	self.client = _client
    	base.disableMouse()
    	base.camera.setPos(15.971, -9.9669, 15.3914)
    	base.camera.setHpr(55.2942, -39.3578, 1.55023)
    	

    def update(self, dt):
        pass
