

"""
.. module:: stun_client
.. role:: red

BitPie.NET stun_client() Automat

.. raw:: html

    <a href="stun_client.png" target="_blank">
    <img src="stun_client.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`datagram-received`
    * :red:`found-one-peer`
    * :red:`peers-not-found`
    * :red:`start`
    * :red:`timer-01sec`
    * :red:`timer-1sec`
"""

import automat

_StunClient = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _StunClient
    if _StunClient is None:
        # set automat name and starting state here
        _StunClient = StunClient('stun_client', 'KNOW_MY_IP')
    if event is not None:
        _StunClient.automat(event, arg)
    return _StunClient


class StunClient(automat.Automat):
    """
    This class implements all the functionality of the ``stun_client()`` state machine.
    """

    timers = {
        'timer-1sec': (1.0, ['REQUEST']),
        'timer-01sec': (0.1, ['REQUEST']),
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
        #---KNOW_MY_IP---
        if self.state == 'KNOW_MY_IP':
            if event == 'start' :
                self.state = 'RANDOM_PEER'
                self.doInit(arg)
                self.doDHTFindRandomNode(arg)
        #---STOPPED---
        elif self.state == 'STOPPED':
            if event == 'start' :
                self.state = 'RANDOM_PEER'
                self.doInit(arg)
                self.doDHTFindRandomNode(arg)
        #---RANDOM_PEER---
        elif self.state == 'RANDOM_PEER':
            if event == 'datagram-received' and self.isMyIPPort(arg) :
                self.state = 'KNOW_MY_IP'
                self.doReportSuccess(arg)
            elif event == 'peers-not-found' :
                self.state = 'STOPPED'
                self.doReportFailed(arg)
            elif event == 'found-one-peer' :
                self.state = 'REQUEST'
                self.doRememberPeer(arg)
                self.doStun(arg)
        #---REQUEST---
        elif self.state == 'REQUEST':
            if event == 'timer-1sec' :
                self.state = 'RANDOM_PEER'
                self.doDHTFindRandomNode(arg)
            elif event == 'datagram-received' and self.isMyIPPort(arg) :
                self.state = 'KNOW_MY_IP'
                self.doReportSuccess(arg)
            elif event == 'timer-01sec' :
                self.doStun(arg)


    def isMyIPPort(self, arg):
        """
        Condition method.
        """

    def doStun(self, arg):
        """
        Action method.
        """

    def doReportSuccess(self, arg):
        """
        Action method.
        """

    def doDHTFindRandomNode(self, arg):
        """
        Action method.
        """

    def doInit(self, arg):
        """
        Action method.
        """

    def doReportFailed(self, arg):
        """
        Action method.
        """

    def doRememberPeer(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

