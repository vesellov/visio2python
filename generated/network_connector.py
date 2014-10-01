

"""
.. module:: network_connector
.. role:: red

BitPie.NET network_connector() Automat

.. raw:: html

    <a href="network_connector.png" target="_blank">
    <img src="network_connector.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`all-transports-ready`
    * :red:`connection-done`
    * :red:`got-network-info`
    * :red:`init`
    * :red:`internet-failed`
    * :red:`internet-success`
    * :red:`network-down`
    * :red:`network-up`
    * :red:`reconnect`
    * :red:`timer-1hour`
    * :red:`timer-20sec`
    * :red:`timer-5sec`
    * :red:`upnp-done`
"""

import automat

_NetworkConnector = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _NetworkConnector
    if _NetworkConnector is None:
        # set automat name and starting state here
        _NetworkConnector = NetworkConnector('network_connector', 'GATE_INIT')
    if event is not None:
        _NetworkConnector.automat(event, arg)
    return _NetworkConnector


class NetworkConnector(automat.Automat):
    """
    This class implements all the functionality of the ``network_connector()`` state machine.
    """

    timers = {
        'timer-1hour': (3600, ['DISCONNECTED']),
        'timer-5sec': (5.0, ['DISCONNECTED','CONNECTED']),
        'timer-20sec': (20.0, ['GATE_INIT']),
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
        #---GATE_INIT---
        if self.state == 'GATE_INIT':
            if event == 'timer-20sec' or event == 'all-transports-ready' :
                self.state = 'UP'
                self.doSetUp(arg)
                self.Disconnects=0
                self.Reset=False
        #---UP---
        elif self.state == 'UP':
            if event == 'network-up' and not self.isNeedUPNP(arg) :
                self.state = 'CONNECTED'
                stun_client.A('start')
            elif event == 'reconnect' :
                self.Reset=True
            elif event == 'network-up' and self.isNeedUPNP(arg) :
                self.state = 'UPNP'
                self.doUPNP(arg)
        #---DISCONNECTED---
        elif self.state == 'DISCONNECTED':
            if event == 'reconnect' or event == 'timer-1hour' or ( event == 'timer-5sec' and ( self.Disconnects < 3 or self.Reset ) ) or ( event == 'connection-done' and self.isTimePassed(arg) ) :
                self.state = 'DOWN'
                self.doRememberTime(arg)
                self.Disconnects+=1
                self.Reset=False
                self.doSetDown(arg)
        #---CONNECTED---
        elif self.state == 'CONNECTED':
            if event == 'reconnect' or ( event == 'timer-5sec' and ( self.Reset or not self.isConnectionAlive(arg) ) ) :
                self.state = 'DOWN'
                self.Disconnects=0
                self.Reset=False
                self.doSetDown(arg)
        #---UPNP---
        elif self.state == 'UPNP':
            if event == 'reconnect' :
                self.Reset=True
            elif event == 'upnp-done' :
                self.state = 'CONNECTED'
                stun_client.A('start')
        #---NETWORK?---
        elif self.state == 'NETWORK?':
            if event == 'got-network-info' and self.isNetworkActive(arg) and self.isCurrentInterfaceActive(arg) :
                self.state = 'INTERNET?'
                self.doPingGoogleDotCom(arg)
            elif event == 'got-network-info' and self.isNetworkActive(arg) and not self.isCurrentInterfaceActive(arg) :
                self.state = 'UP'
                self.doSetUp(arg)
            elif event == 'got-network-info' and not self.isNetworkActive(arg) :
                self.state = 'DISCONNECTED'
        #---AT_STARTUP---
        elif self.state == 'AT_STARTUP':
            if event == 'init' :
                self.state = 'GATE_INIT'
                self.doInitGate(arg)
        #---INTERNET?---
        elif self.state == 'INTERNET?':
            if event == 'internet-success' :
                self.state = 'UP'
                self.doSetUp(arg)
            elif event == 'internet-failed' :
                self.state = 'DISCONNECTED'
        #---DOWN---
        elif self.state == 'DOWN':
            if event == 'network-down' :
                self.state = 'NETWORK?'
                self.doCheckNetworkInterfaces(arg)


    def isNetworkActive(self, arg):
        """
        Condition method.
        """

    def isCurrentInterfaceActive(self, arg):
        """
        Condition method.
        """

    def isTimePassed(self, arg):
        """
        Condition method.
        """

    def isNeedUPNP(self, arg):
        """
        Condition method.
        """

    def isConnectionAlive(self, arg):
        """
        Condition method.
        """

    def doRememberTime(self, arg):
        """
        Action method.
        """

    def doUPNP(self, arg):
        """
        Action method.
        """

    def doInitGate(self, arg):
        """
        Action method.
        """

    def doSetUp(self, arg):
        """
        Action method.
        """

    def doCheckNetworkInterfaces(self, arg):
        """
        Action method.
        """

    def doPingGoogleDotCom(self, arg):
        """
        Action method.
        """

    def doSetDown(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

