

"""
.. module:: stun_server
.. role:: red

BitPie.NET stun_server() Automat

.. raw:: html

    <a href="stun_server.png" target="_blank">
    <img src="stun_server.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`datagram-received`
    * :red:`start`
    * :red:`stop`
"""

import automat

_StunServer = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _StunServer
    if _StunServer is None:
        # set automat name and starting state here
        _StunServer = StunServer('stun_server', 'AT_STARTUP')
    if event is not None:
        _StunServer.automat(event, arg)
    return _StunServer


class StunServer(automat.Automat):
    """
    This class implements all the functionality of the ``stun_server()`` state machine.
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
                self.state = 'LISTEN'
                self.doInit(arg)
        #---LISTEN---
        elif self.state == 'LISTEN':
            if event == 'datagram-received' and self.isSTUN(arg) :
                self.doSendYourIPPort(arg)
            elif event == 'stop' :
                self.state = 'STOPPED'
                self.doStop(arg)
        #---STOPPED---
        elif self.state == 'STOPPED':
            if event == 'start' :
                self.state = 'LISTEN'
                self.doInit(arg)


    def isSTUN(self, arg):
        """
        Condition method.
        """

    def doSendYourIPPort(self, arg):
        """
        Action method.
        """

    def doInit(self, arg):
        """
        Action method.
        """

    def doStop(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

