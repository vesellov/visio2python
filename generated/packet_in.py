

"""
.. module:: packet_in
.. role:: red

BitPie.NET packet_in() Automat

.. raw:: html

    <a href="packet_in.png" target="_blank">
    <img src="packet_in.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`cancel`
    * :red:`failed`
    * :red:`register-item`
    * :red:`remote-id-cached`
    * :red:`unregister-item`
    * :red:`unserialize-failed`
    * :red:`valid-inbox-packet`
"""

import automat

_PacketIn = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _PacketIn
    if _PacketIn is None:
        # set automat name and starting state here
        _PacketIn = PacketIn('packet_in', 'AT_STARTUP')
    if event is not None:
        _PacketIn.automat(event, arg)
    return _PacketIn


class PacketIn(automat.Automat):
    """
    This class implements all the functionality of the ``packet_in()`` state machine.
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
            if event == 'register-item' :
                self.state = 'RECEIVING'
                self.doInit(arg)
        #---RECEIVING---
        elif self.state == 'RECEIVING':
            if event == 'unregister-item' and not self.isTransferFinished(arg) :
                self.state = 'FAILED'
                self.doReportFailed(arg)
                self.doEraseInputFile(arg)
                self.doDestroyMe(arg)
            elif event == 'unregister-item' and self.isTransferFinished(arg) and not self.isRemoteIdentityCached(arg) :
                self.state = 'CACHING'
                self.doCacheRemoteIdentity(arg)
            elif event == 'cancel' :
                self.doCancelItem(arg)
            elif event == 'unregister-item' and self.isTransferFinished(arg) and self.isRemoteIdentityCached(arg) :
                self.state = 'INBOX?'
                self.doReadAndUnserialize(arg)
        #---INBOX?---
        elif self.state == 'INBOX?':
            if event == 'valid-inbox-packet' :
                self.state = 'DONE'
                self.doReportReceived(arg)
                self.doEraseInputFile(arg)
                self.doDestroyMe(arg)
            elif event == 'unserialize-failed' :
                self.state = 'FAILED'
                self.doReportFailed(arg)
                self.doEraseInputFile(arg)
                self.doDestroyMe(arg)
        #---FAILED---
        elif self.state == 'FAILED':
            pass
        #---DONE---
        elif self.state == 'DONE':
            pass
        #---CACHING---
        elif self.state == 'CACHING':
            if event == 'failed' :
                self.state = 'FAILED'
                self.doReportCacheFailed(arg)
                self.doEraseInputFile(arg)
                self.doDestroyMe(arg)
            elif event == 'remote-id-cached' :
                self.state = 'INBOX?'
                self.doReadAndUnserialize(arg)


    def isTransferFinished(self, arg):
        """
        Condition method.
        """

    def isRemoteIdentityCached(self, arg):
        """
        Condition method.
        """

    def doReportFailed(self, arg):
        """
        Action method.
        """

    def doEraseInputFile(self, arg):
        """
        Action method.
        """

    def doReportReceived(self, arg):
        """
        Action method.
        """

    def doReadAndUnserialize(self, arg):
        """
        Action method.
        """

    def doReportCacheFailed(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _PacketIn
        del _PacketIn
        _PacketIn = None

    def doCancelItem(self, arg):
        """
        Action method.
        """

    def doInit(self, arg):
        """
        Action method.
        """

    def doCacheRemoteIdentity(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

