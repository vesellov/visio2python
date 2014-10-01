

"""
.. module:: udp_node
.. role:: red

BitPie.NET udp_node() Automat

.. raw:: html

    <a href="udp_node.png" target="_blank">
    <img src="udp_node.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`connect`
    * :red:`datagram-received`
    * :red:`dht-read-result`
    * :red:`dht-write-failed`
    * :red:`dht-write-success`
    * :red:`disconnected`
    * :red:`go-offline`
    * :red:`go-online`
    * :red:`stun-failed`
    * :red:`stun-success`
    * :red:`timer-10sec`
"""

import automat

_UdpNode = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _UdpNode
    if _UdpNode is None:
        # set automat name and starting state here
        _UdpNode = UdpNode('udp_node', 'AT_STARTUP')
    if event is not None:
        _UdpNode.automat(event, arg)
    return _UdpNode


class UdpNode(automat.Automat):
    """
    This class implements all the functionality of the ``udp_node()`` state machine.
    """

    timers = {
        'timer-10sec': (10.0, ['LISTEN']),
        }

    def init(self):
        """
        Method to initialize additional variables and flags at creation of the state machine.
        """

    def state_changed(self, oldstate, newstate):
        """
        Method to to catch the moment when automat's state were changed.
        """

    def A(self, event, arg):
        """
        The state machine code, generated using `visio2python <http://code.google.com/p/visio2python/>`_ tool.
        """
        #---AT_STARTUP---
        if self.state == 'AT_STARTUP':
            if event == 'go-online' :
                self.state = 'STUN'
                self.GoOn=False
                self.doInit(arg)
                self.doStartStunClient(arg)
        #---STUN---
        elif self.state == 'STUN':
            if event == 'datagram-received' and self.isPacketValid(arg) and not self.isStun(arg) and not self.isKnownPeer(arg) :
                pass
            elif event == 'stun-success' :
                self.state = 'WRITE_MY_IP'
                self.doUpdateMyAddress(arg)
                self.doDHTWtiteMyAddress(arg)
            elif event == 'stun-failed' :
                self.state = 'OFFLINE'
                self.doUpdateMyAddress(arg)
                self.doNotifyFailed(arg)
            elif event == 'go-offline' :
                self.state = 'DISCONNECTING'
                self.doDisconnect(arg)
        #---LISTEN---
        elif self.state == 'LISTEN':
            if event == 'datagram-received' and self.isPacketValid(arg) and not self.isStun(arg) and not self.isKnownPeer(arg) :
                self.doStartNewSession(arg)
            elif event == 'timer-10sec' and self.isKnowMyAddress(arg) :
                self.state = 'WRITE_MY_IP'
                self.doDHTWtiteMyAddress(arg)
            elif event == 'connect' and self.isKnowMyAddress(arg) and not self.isKnownUser(arg) :
                self.doStartNewConnector(arg)
            elif event == 'go-offline' :
                self.state = 'DISCONNECTING'
                self.doDisconnect(arg)
            elif event == 'timer-10sec' and not self.isKnowMyAddress(arg) :
                self.state = 'STUN'
                self.doStartStunClient(arg)
        #---OFFLINE---
        elif self.state == 'OFFLINE':
            if event == 'go-online' :
                self.state = 'STUN'
                self.doStartStunClient(arg)
        #---DISCONNECTING---
        elif self.state == 'DISCONNECTING':
            if event == 'go-online' :
                self.GoOn=True
            elif event == 'disconnected' and not self.GoOn :
                self.state = 'OFFLINE'
                self.doNotifyDisconnected(arg)
            elif event == 'disconnected' and self.GoOn :
                self.state = 'STUN'
                self.GoOn=False
                self.doNotifyDisconnected(arg)
                self.doStartStunClient(arg)
        #---DHT_READ---
        elif self.state == 'DHT_READ':
            if event == 'datagram-received' and self.isPacketValid(arg) and not self.isStun(arg) and not self.isKnownPeer(arg) :
                pass
            elif event == 'connect' and not self.isKnowMyAddress(arg) :
                self.state = 'STUN'
                self.doStartStunClient(arg)
            elif event == 'dht-read-result' :
                self.state = 'LISTEN'
                self.doCheckAndStartNewSessions(arg)
                self.doDHTRemoveMyIncomings(arg)
                self.doNotifyConnected(arg)
            elif event == 'connect' and self.isKnowMyAddress(arg) and not self.isKnownUser(arg) :
                self.doStartNewConnector(arg)
            elif event == 'go-offline' :
                self.state = 'DISCONNECTING'
                self.doDisconnect(arg)
        #---WRITE_MY_IP---
        elif self.state == 'WRITE_MY_IP':
            if event == 'dht-write-failed' :
                self.state = 'OFFLINE'
                self.doNotifyFailed(arg)
            elif event == 'connect' and not self.isKnowMyAddress(arg) :
                self.state = 'STUN'
                self.doStartStunClient(arg)
            elif event == 'connect' and self.isKnowMyAddress(arg) and not self.isKnownUser(arg) :
                self.doStartNewConnector(arg)
            elif event == 'datagram-received' and self.isPacketValid(arg) and not self.isStun(arg) and not self.isKnownPeer(arg) :
                pass
            elif event == 'go-offline' :
                self.state = 'DISCONNECTING'
                self.doDisconnect(arg)
            elif event == 'dht-write-success' :
                self.state = 'DHT_READ'
                self.doDHTReadMyIncomings(arg)


    def isKnownUser(self, arg):
        """
        Condition method.
        """

    def isStun(self, arg):
        """
        Condition method.
        """

    def isKnowMyAddress(self, arg):
        """
        Condition method.
        """

    def isPacketValid(self, arg):
        """
        Condition method.
        """

    def isKnownPeer(self, arg):
        """
        Condition method.
        """

    def doUpdateMyAddress(self, arg):
        """
        Action method.
        """

    def doDisconnect(self, arg):
        """
        Action method.
        """

    def doDHTWtiteMyAddress(self, arg):
        """
        Action method.
        """

    def doDHTRemoveMyIncomings(self, arg):
        """
        Action method.
        """

    def doNotifyDisconnected(self, arg):
        """
        Action method.
        """

    def doStartNewConnector(self, arg):
        """
        Action method.
        """

    def doCheckAndStartNewSessions(self, arg):
        """
        Action method.
        """

    def doNotifyConnected(self, arg):
        """
        Action method.
        """

    def doStartStunClient(self, arg):
        """
        Action method.
        """

    def doStartNewSession(self, arg):
        """
        Action method.
        """

    def doNotifyFailed(self, arg):
        """
        Action method.
        """

    def doDHTReadMyIncomings(self, arg):
        """
        Action method.
        """

    def doInit(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

