

"""
.. module:: udp_stream
.. role:: red

BitPie.NET udp_stream() Automat  [fast, post]

.. raw:: html

    <a href="udp_stream.png" target="_blank">
    <img src="udp_stream.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`ack-received`
    * :red:`block-received`
    * :red:`close`
    * :red:`consume`
    * :red:`init`
    * :red:`iterate`
    * :red:`resume`
    * :red:`set-limits`
    * :red:`timeout`
"""

import automat

_UdpStream = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _UdpStream
    if _UdpStream is None:
        # set automat name and starting state here
        _UdpStream = UdpStream('udp_stream', 'SENDING')
    if event is not None:
        _UdpStream.automat(event, arg)
    return _UdpStream


class UdpStream(automat.Automat):
    """
    This class implements all the functionality of the ``udp_stream()`` state machine.
    """

    fast = True

    post = True

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
        newstate = self.state
        #---SENDING---
        if self.state == 'SENDING':
            if event == 'ack-received' and not self.isPaused(arg) and not ( self.isZeroAck(arg) or self.isWriteEOF(arg) ) :
                self.doResendBlocks(arg)
                self.doSendingLoop(arg)
            elif event == 'iterate' :
                self.doResendBlocks(arg)
                self.doSendingLoop(arg)
            elif event == 'consume' :
                self.doPushBlocks(arg)
                self.doResendBlocks(arg)
                self.doSendingLoop(arg)
            elif event == 'set-limits' :
                self.doUpdateLimits(arg)
            elif event == 'ack-received' and ( self.isZeroAck(arg) or self.isWriteEOF(arg) ) :
                self.doReportSendDone(arg)
                self.doCloseStream(arg)
                newstate = 'COMPLETION'
            elif event == 'ack-received' and self.isPaused(arg) :
                self.doResumeLater(arg)
                newstate = 'PAUSE'
            elif event == 'timeout' :
                self.doReportSendTimeout(arg)
                self.doCloseStream(arg)
                newstate = 'COMPLETION'
            elif event == 'close' :
                self.doReportClosed(arg)
                self.doCloseStream(arg)
                self.doDestroyMe(arg)
                newstate = 'CLOSED'
        #---DOWNTIME---
        elif self.state == 'DOWNTIME':
            if event == 'block-received' :
                self.doResendAck(arg)
                self.doReceivingLoop(arg)
                newstate = 'RECEIVING'
            elif event == 'close' :
                self.doReportClosed(arg)
                self.doCloseStream(arg)
                self.doDestroyMe(arg)
                newstate = 'CLOSED'
            elif event == 'ack-received' :
                self.doReportError(arg)
                self.doCloseStream(arg)
                newstate = 'COMPLETION'
            elif event == 'consume' :
                self.doPushBlocks(arg)
                self.doResendBlocks(arg)
                self.doSendingLoop(arg)
                newstate = 'SENDING'
            elif event == 'set-limits' :
                self.doUpdateLimits(arg)
        #---AT_STARTUP---
        elif self.state == 'AT_STARTUP':
            if event == 'init' :
                self.doInit(arg)
                newstate = 'DOWNTIME'
        #---RECEIVING---
        elif self.state == 'RECEIVING':
            if event == 'set-limits' :
                self.doUpdateLimits(arg)
            elif event == 'block-received' and self.isReadEOF(arg) :
                self.doResendAck(arg)
                self.doSendZeroAck(arg)
                self.doReportReceiveDone(arg)
                self.doCloseStream(arg)
                newstate = 'COMPLETION'
            elif event == 'timeout' :
                self.doReportReceiveTimeout(arg)
                self.doCloseStream(arg)
                newstate = 'COMPLETION'
            elif event == 'iterate' :
                self.doResendAck(arg)
                self.doReceivingLoop(arg)
            elif event == 'block-received' and not self.isReadEOF(arg) :
                self.doResendAck(arg)
                self.doReceivingLoop(arg)
            elif event == 'close' :
                self.doReportClosed(arg)
                self.doCloseStream(arg)
                self.doDestroyMe(arg)
                newstate = 'CLOSED'
        #---COMPLETION---
        elif self.state == 'COMPLETION':
            if event == 'close' :
                self.doDestroyMe(arg)
                newstate = 'CLOSED'
        #---CLOSED---
        elif self.state == 'CLOSED':
            pass
        #---PAUSE---
        elif self.state == 'PAUSE':
            if event == 'consume' :
                self.doPushBlocks(arg)
            elif event == 'ack-received' and ( self.isZeroAck(arg) or self.isWriteEOF(arg) ) :
                self.doReportSendDone(arg)
                self.doCloseStream(arg)
                newstate = 'COMPLETION'
            elif event == 'resume' :
                self.doResendBlocks(arg)
                self.doSendingLoop(arg)
                newstate = 'SENDING'
            elif event == 'close' :
                self.doReportClosed(arg)
                self.doCloseStream(arg)
                self.doDestroyMe(arg)
                newstate = 'CLOSED'
            elif event == 'timeout' :
                self.doReportSendTimeout(arg)
                self.doCloseStream(arg)
                newstate = 'COMPLETION'
        return newstate


    def isPaused(self, arg):
        """
        Condition method.
        """

    def isReadEOF(self, arg):
        """
        Condition method.
        """

    def isWriteEOF(self, arg):
        """
        Condition method.
        """

    def isZeroAck(self, arg):
        """
        Condition method.
        """

    def doReportSendTimeout(self, arg):
        """
        Action method.
        """

    def doSendingLoop(self, arg):
        """
        Action method.
        """

    def doReportSendDone(self, arg):
        """
        Action method.
        """

    def doPushBlocks(self, arg):
        """
        Action method.
        """

    def doReportClosed(self, arg):
        """
        Action method.
        """

    def doReportReceiveDone(self, arg):
        """
        Action method.
        """

    def doSendZeroAck(self, arg):
        """
        Action method.
        """

    def doReportReceiveTimeout(self, arg):
        """
        Action method.
        """

    def doReportError(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _UdpStream
        del _UdpStream
        _UdpStream = None

    def doCloseStream(self, arg):
        """
        Action method.
        """

    def doResumeLater(self, arg):
        """
        Action method.
        """

    def doUpdateLimits(self, arg):
        """
        Action method.
        """

    def doInit(self, arg):
        """
        Action method.
        """

    def doReceivingLoop(self, arg):
        """
        Action method.
        """

    def doResendBlocks(self, arg):
        """
        Action method.
        """

    def doResendAck(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

