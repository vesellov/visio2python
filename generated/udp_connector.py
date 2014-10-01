

"""
.. module:: udp_connector
.. role:: red

BitPie.NET udp_connector() Automat

.. raw:: html

    <a href="udp_connector.png" target="_blank">
    <img src="udp_connector.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`dht-read-failed`
    * :red:`dht-read-success`
    * :red:`dht-write-failed`
    * :red:`dht-write-success`
    * :red:`start`
"""

import automat

_UdpConnector = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _UdpConnector
    if _UdpConnector is None:
        # set automat name and starting state here
        _UdpConnector = UdpConnector('udp_connector', 'AT_STARTUP')
    if event is not None:
        _UdpConnector.automat(event, arg)
    return _UdpConnector


class UdpConnector(automat.Automat):
    """
    This class implements all the functionality of the ``udp_connector()`` state machine.
    """

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
            if event == 'start' :
                self.state = 'DHT_WRITE'
                self.doInit(arg)
                self.doDHTWritePeerIncomings(arg)
        #---DHT_WRITE---
        elif self.state == 'DHT_WRITE':
            if event == 'dht-write-success' :
                self.state = 'DHT_READ'
                self.doDHTReadPeerAddress(arg)
            elif event == 'dht-write-failed' :
                self.state = 'FAILED'
                self.doDestroyMe(arg)
        #---DHT_READ---
        elif self.state == 'DHT_READ':
            if event == 'dht-read-success' :
                self.state = 'DONE'
                self.doStartNewSession(arg)
                self.doDestroyMe(arg)
            elif event == 'dht-read-failed' :
                self.state = 'FAILED'
                self.doDestroyMe(arg)
        #---DONE---
        elif self.state == 'DONE':
            pass
        #---FAILED---
        elif self.state == 'FAILED':
            pass


    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _UdpConnector
        del _UdpConnector
        _UdpConnector = None

    def doInit(self, arg):
        """
        Action method.
        """

    def doDHTWritePeerIncomings(self, arg):
        """
        Action method.
        """

    def doStartNewSession(self, arg):
        """
        Action method.
        """

    def doDHTReadPeerAddress(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

