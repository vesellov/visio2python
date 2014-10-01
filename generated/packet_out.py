

"""
.. module:: packet_out
.. role:: red

BitPie.NET packet_out() Automat

.. raw:: html

    <a href="packet_out.png" target="_blank">
    <img src="packet_out.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`cancel`
    * :red:`failed`
    * :red:`inbox-packet`
    * :red:`item-cancelled`
    * :red:`items-sent`
    * :red:`nothing-to-send`
    * :red:`register-item`
    * :red:`remote-identity-on-hand`
    * :red:`run`
    * :red:`unregister-item`
    * :red:`write-error`
"""

import automat

_PacketOut = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _PacketOut
    if _PacketOut is None:
        # set automat name and starting state here
        _PacketOut = PacketOut('packet_out', 'SENDING')
    if event is not None:
        _PacketOut.automat(event, arg)
    return _PacketOut


class PacketOut(automat.Automat):
    """
    This class implements all the functionality of the ``packet_out()`` state machine.
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
        #---SENDING---
        if self.state == 'SENDING':
            if ( event == 'unregister-item' or event == 'item-cancelled' ) and self.isMoreItems(arg) :
                self.doPopItem(arg)
                self.doReportItem(arg)
            elif event == 'inbox-packet' and self.isResponse(arg) :
                self.Acked=True
                self.doSaveResponse(arg)
            elif event == 'unregister-item' and not self.isMoreItems(arg) and self.isAckNeeded(arg) and not self.Acked :
                self.state = 'RESPONSE?'
                self.doPopItem(arg)
                self.doReportItem(arg)
            elif event == 'register-item' :
                self.doSetTransferID(arg)
            elif ( event == 'unregister-item' or event == 'item-cancelled' ) and not self.isMoreItems(arg) and ( self.Acked or not self.isAckNeeded(arg) ) :
                self.state = 'SENT'
                self.doPopItem(arg)
                self.doReportItem(arg)
                self.doReportDoneNoAck(arg)
                self.doDestroyMe(arg)
            elif event == 'cancel' :
                self.state = 'CANCEL'
                self.doCancelItems(arg)
                self.doReportCancelItems(arg)
                self.doPopItems(arg)
                self.doReportCancelled(arg)
                self.doDestroyMe(arg)
        #---AT_STARTUP---
        elif self.state == 'AT_STARTUP':
            if event == 'run' and self.isRemoteIdentityKnown(arg) :
                self.state = 'ITEMS?'
                self.doInit(arg)
                self.doReportStarted(arg)
                self.doSerializeAndWrite(arg)
                self.doPushItems(arg)
            elif event == 'run' and not self.isRemoteIdentityKnown(arg) :
                self.state = 'CACHING'
                self.doInit(arg)
                self.doCacheRemoteIdentity(arg)
        #---CACHING---
        elif self.state == 'CACHING':
            if event == 'remote-identity-on-hand' :
                self.state = 'ITEMS?'
                self.doReportStarted(arg)
                self.doSerializeAndWrite(arg)
                self.doPushItems(arg)
            elif event == 'failed' :
                self.state = 'FAILED'
                self.doReportFailed(arg)
                self.doDestroyMe(arg)
        #---FAILED---
        elif self.state == 'FAILED':
            pass
        #---ITEMS?---
        elif self.state == 'ITEMS?':
            if event == 'items-sent' :
                self.state = 'IN_QUEUE'
            elif event == 'nothing-to-send' or event == 'write-error' :
                self.state = 'FAILED'
                self.doReportFailed(arg)
                self.doDestroyMe(arg)
        #---IN_QUEUE---
        elif self.state == 'IN_QUEUE':
            if event == 'register-item' :
                self.state = 'SENDING'
                self.Acked=False
                self.doSetTransferID(arg)
            elif event == 'item-cancelled' and self.isMoreItems(arg) :
                self.doPopItem(arg)
            elif event == 'cancel' :
                self.state = 'CANCEL'
                self.doCancelItems(arg)
                self.doReportCancelItems(arg)
                self.doPopItems(arg)
                self.doReportCancelled(arg)
                self.doDestroyMe(arg)
            elif event == 'item-cancelled' and not self.isMoreItems(arg) :
                self.state = 'FAILED'
                self.doPopItem(arg)
                self.doReportItem(arg)
                self.doReportFailed(arg)
                self.doDestroyMe(arg)
        #---RESPONSE?---
        elif self.state == 'RESPONSE?':
            if event == 'cancel' :
                self.state = 'CANCEL'
                self.doReportCancelItems(arg)
                self.doReportCancelled(arg)
                self.doDestroyMe(arg)
            elif event == 'inbox-packet' and self.isResponse(arg) :
                self.state = 'SENT'
                self.doSaveResponse(arg)
                self.doReportDoneWithAck(arg)
                self.doDestroyMe(arg)
        #---SENT---
        elif self.state == 'SENT':
            pass
        #---CANCEL---
        elif self.state == 'CANCEL':
            pass


    def isRemoteIdentityKnown(self, arg):
        """
        Condition method.
        """

    def isMoreItems(self, arg):
        """
        Condition method.
        """

    def isAckNeeded(self, arg):
        """
        Condition method.
        """

    def isResponse(self, arg):
        """
        Condition method.
        """

    def doReportDoneWithAck(self, arg):
        """
        Action method.
        """

    def doPushItems(self, arg):
        """
        Action method.
        """

    def doCancelItems(self, arg):
        """
        Action method.
        """

    def doReportStarted(self, arg):
        """
        Action method.
        """

    def doReportItem(self, arg):
        """
        Action method.
        """

    def doReportCancelled(self, arg):
        """
        Action method.
        """

    def doPopItem(self, arg):
        """
        Action method.
        """

    def doPopItems(self, arg):
        """
        Action method.
        """

    def doSerializeAndWrite(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _PacketOut
        del _PacketOut
        _PacketOut = None

    def doSetTransferID(self, arg):
        """
        Action method.
        """

    def doReportDoneNoAck(self, arg):
        """
        Action method.
        """

    def doCacheRemoteIdentity(self, arg):
        """
        Action method.
        """

    def doInit(self, arg):
        """
        Action method.
        """

    def doReportCancelItems(self, arg):
        """
        Action method.
        """

    def doReportFailed(self, arg):
        """
        Action method.
        """

    def doSaveResponse(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

