

"""
.. module:: udp_session
.. role:: red

BitPie.NET udp_session() Automat

.. raw:: html

    <a href="udp_session.png" target="_blank">
    <img src="udp_session.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`datagram-received`
    * :red:`init`
    * :red:`shutdown`
    * :red:`timer-10sec`
    * :red:`timer-1min`
    * :red:`timer-1sec`
    * :red:`timer-30sec`
"""

import automat

_UdpSession = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _UdpSession
    if _UdpSession is None:
        # set automat name and starting state here
        _UdpSession = UdpSession('udp_session', 'AT_STARTUP')
    if event is not None:
        _UdpSession.automat(event, arg)
    return _UdpSession


class UdpSession(automat.Automat):
    """
    This class implements all the functionality of the ``udp_session()`` state machine.
    """

    timers = {
        'timer-1min': (60, ['CONNECTED']),
        'timer-1sec': (1.0, ['PING','GREETING']),
        'timer-30sec': (30.0, ['GREETING']),
        'timer-10sec': (10.0, ['PING','CONNECTED']),
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
            if event == 'init' :
                self.state = 'PING'
                self.doInit(arg)
                self.doPing(arg)
            elif event == 'shutdown' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
        #---PING---
        elif self.state == 'PING':
            if event == 'datagram-received' and self.isPing(arg) :
                self.state = 'GREETING'
                self.doReceiveData(arg)
            elif event == 'shutdown' or event == 'timer-10sec' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'datagram-received' and self.isGreeting(arg) :
                self.state = 'GREETING'
                self.doReceiveData(arg)
            elif event == 'timer-1sec' :
                self.doPing(arg)
            elif event == 'datagram-received' and not self.isPingOrGreeting(arg) :
                pass
        #---GREETING---
        elif self.state == 'GREETING':
            if event == 'shutdown' or event == 'timer-30sec' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'timer-1sec' :
                self.doGreeting(arg)
            elif event == 'datagram-received' and self.isGreetingOrAlive(arg) :
                self.state = 'CONNECTED'
                self.doReceiveData(arg)
                self.doNotifyConnected(arg)
                self.doCheckPendingFiles(arg)
            elif event == 'datagram-received' and not self.isGreetingOrAlive(arg) :
                pass
        #---CONNECTED---
        elif self.state == 'CONNECTED':
            if event == 'shutdown' or ( event == 'timer-1min' and not self.isSessionActive(arg) ) :
                self.state = 'CLOSED'
                self.doNotifyDisconnected(arg)
                self.doDestroyMe(arg)
            elif event == 'timer-10sec' :
                self.doAlive(arg)
            elif event == 'datagram-received' :
                self.doReceiveData(arg)
        #---CLOSED---
        elif self.state == 'CLOSED':
            pass


    def isPing(self, arg):
        """
        Condition method.
        """

    def isSessionActive(self, arg):
        """
        Condition method.
        """

    def isPingOrGreeting(self, arg):
        """
        Condition method.
        """

    def isGreeting(self, arg):
        """
        Condition method.
        """

    def isGreetingOrAlive(self, arg):
        """
        Condition method.
        """

    def doNotifyDisconnected(self, arg):
        """
        Action method.
        """

    def doCheckPendingFiles(self, arg):
        """
        Action method.
        """

    def doGreeting(self, arg):
        """
        Action method.
        """

    def doPing(self, arg):
        """
        Action method.
        """

    def doAlive(self, arg):
        """
        Action method.
        """

    def doReceiveData(self, arg):
        """
        Action method.
        """

    def doNotifyConnected(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _UdpSession
        del _UdpSession
        _UdpSession = None

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

