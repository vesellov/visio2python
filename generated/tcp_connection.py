

"""
.. module:: tcp_connection
.. role:: red

BitPie.NET tcp_connection() Automat

.. raw:: html

    <a href="tcp_connection.png" target="_blank">
    <img src="tcp_connection.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`connection-lost`
    * :red:`connection-made`
    * :red:`data-received`
    * :red:`disconnect`
    * :red:`timer-10sec`
"""

import automat

_TcpConnection = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _TcpConnection
    if _TcpConnection is None:
        # set automat name and starting state here
        _TcpConnection = TcpConnection('tcp_connection', 'AT_STARTUP')
    if event is not None:
        _TcpConnection.automat(event, arg)
    return _TcpConnection


class TcpConnection(automat.Automat):
    """
    This class implements all the functionality of the ``tcp_connection()`` state machine.
    """

    timers = {
        'timer-10sec': (10.0, ['CLIENT?','SERVER?']),
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
            if event == 'connection-made' and not self.isOutgoing(arg) :
                self.state = 'SERVER?'
                self.doInit(arg)
            elif event == 'connection-made' and self.isOutgoing(arg) :
                self.state = 'CLIENT?'
                self.doInit(arg)
                self.doCloseOutgoing(arg)
                self.doSendHello(arg)
        #---CLIENT?---
        elif self.state == 'CLIENT?':
            if event == 'timer-10sec' or event == 'disconnect' or ( event == 'data-received' and not ( self.isWazap(arg) and self.isSomePendingFiles () ) ) :
                self.state = 'DISCONNECT'
                self.doDisconnect(arg)
            elif event == 'data-received' and self.isWazap(arg) and self.isSomePendingFiles(arg) :
                self.state = 'CONNECTED'
                self.doReadWazap(arg)
                self.doOpenStream(arg)
                self.doStartPendingFiles(arg)
            elif event == 'connection-lost' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
        #---SERVER?---
        elif self.state == 'SERVER?':
            if event == 'timer-10sec' or event == 'disconnect' or ( event == 'data-received' and not self.isHello(arg) ) :
                self.state = 'DISCONNECT'
                self.doDisconnect(arg)
            elif event == 'connection-lost' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'data-received' and self.isHello(arg) :
                self.state = 'CONNECTED'
                self.doReadHello(arg)
                self.doSendWazap(arg)
                self.doOpenStream(arg)
                self.doStartPendingFiles(arg)
        #---CONNECTED---
        elif self.state == 'CONNECTED':
            if event == 'connection-lost' :
                self.state = 'CLOSED'
                self.doStopInOutFiles(arg)
                self.doCloseStream(arg)
                self.doDestroyMe(arg)
            elif event == 'disconnect' :
                self.state = 'DISCONNECT'
                self.doStopInOutFiles(arg)
                self.doCloseStream(arg)
                self.doDisconnect(arg)
            elif event == 'data-received' :
                self.doReceiveData(arg)
        #---CLOSED---
        elif self.state == 'CLOSED':
            pass
        #---DISCONNECT---
        elif self.state == 'DISCONNECT':
            if event == 'connection-lost' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)


    def isHello(self, arg):
        """
        Condition method.
        """

    def isOutgoing(self, arg):
        """
        Condition method.
        """

    def isSomePendingFiles(self, arg):
        """
        Condition method.
        """

    def isWazap(self, arg):
        """
        Condition method.
        """

    def doDisconnect(self, arg):
        """
        Action method.
        """

    def doStopInOutFiles(self, arg):
        """
        Action method.
        """

    def doReadHello(self, arg):
        """
        Action method.
        """

    def doSendHello(self, arg):
        """
        Action method.
        """

    def doCloseOutgoing(self, arg):
        """
        Action method.
        """

    def doStartPendingFiles(self, arg):
        """
        Action method.
        """

    def doReceiveData(self, arg):
        """
        Action method.
        """

    def doSendWazap(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _TcpConnection
        del _TcpConnection
        _TcpConnection = None

    def doCloseStream(self, arg):
        """
        Action method.
        """

    def doOpenStream(self, arg):
        """
        Action method.
        """

    def doReadWazap(self, arg):
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

