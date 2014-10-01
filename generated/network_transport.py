

"""
.. module:: network_transport
.. role:: red

BitPie.NET network_transport() Automat

.. raw:: html

    <a href="network_transport.png" target="_blank">
    <img src="network_transport.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`failed`
    * :red:`init`
    * :red:`receiving-started`
    * :red:`shutdown`
    * :red:`start`
    * :red:`stop`
    * :red:`stopped`
    * :red:`transport-initialized`
"""

import automat

_NetworkTransport = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _NetworkTransport
    if _NetworkTransport is None:
        # set automat name and starting state here
        _NetworkTransport = NetworkTransport('network_transport', 'AT_STARTUP')
    if event is not None:
        _NetworkTransport.automat(event, arg)
    return _NetworkTransport


class NetworkTransport(automat.Automat):
    """
    This class implements all the functionality of the ``network_transport()`` state machine.
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
            if event == 'init' :
                self.state = 'INIT'
                self.StartNow=False
                self.StopNow=False
                self.doInit(arg)
        #---STARTING---
        elif self.state == 'STARTING':
            if event == 'shutdown' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'receiving-started' and not self.StopNow :
                self.state = 'LISTENING'
            elif event == 'failed' :
                self.state = 'OFFLINE'
            elif event == 'stop' :
                self.StopNow=True
            elif event == 'receiving-started' and self.StopNow :
                self.state = 'STOPPING'
                self.StopNow=False
                self.doStop(arg)
        #---LISTENING---
        elif self.state == 'LISTENING':
            if event == 'shutdown' :
                self.state = 'CLOSED'
                self.doStop(arg)
                self.doDestroyMe(arg)
            elif event == 'stop' :
                self.state = 'STOPPING'
                self.StopNow=False
                self.doStop(arg)
        #---OFFLINE---
        elif self.state == 'OFFLINE':
            if event == 'shutdown' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'start' :
                self.state = 'STARTING'
                self.StartNow=False
                self.doStart(arg)
        #---STOPPING---
        elif self.state == 'STOPPING':
            if event == 'shutdown' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'stopped' and not self.StartNow :
                self.state = 'OFFLINE'
            elif event == 'start' :
                self.StartNow=True
            elif event == 'stopped' and self.StartNow :
                self.state = 'STARTING'
                self.StartNow=False
                self.doStart(arg)
        #---CLOSED---
        elif self.state == 'CLOSED':
            pass
        #---INIT---
        elif self.state == 'INIT':
            if event == 'start' :
                self.StartNow=True
            elif event == 'transport-initialized' and self.StartNow :
                self.state = 'STARTING'
                self.doCreateProxy(arg)
                self.StartNow=False
                self.doStart(arg)
            elif event == 'transport-initialized' and not self.StartNow :
                self.state = 'OFFLINE'
                self.doCreateProxy(arg)
            elif event == 'shutdown' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)


    def doInit(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _NetworkTransport
        del _NetworkTransport
        _NetworkTransport = None

    def doStop(self, arg):
        """
        Action method.
        """

    def doCreateProxy(self, arg):
        """
        Action method.
        """

    def doStart(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

