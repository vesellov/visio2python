

"""
.. module:: restore
.. role:: red

BitPie.NET restore() Automat

.. raw:: html

    <a href="restore.png" target="_blank">
    <img src="restore.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`block-restored`
    * :red:`init`
    * :red:`packet-came-in`
    * :red:`raid-done`
    * :red:`request-done`
    * :red:`timer-01sec`
    * :red:`timer-1sec`
    * :red:`timer-5sec`
"""

import automat

_Restore = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _Restore
    if _Restore is None:
        # set automat name and starting state here
        _Restore = Restore('restore', 'AT_STARTUP')
    if event is not None:
        _Restore.automat(event, arg)
    return _Restore


class Restore(automat.Automat):
    """
    This class implements all the functionality of the ``restore()`` state machine.
    """

    timers = {
        'timer-1sec': (1.0, ['REQUEST']),
        'timer-01sec': (0.1, ['RUN']),
        'timer-5sec': (5.0, ['REQUEST']),
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
                self.state = 'RUN'
        #---ABORTED---
        elif self.state == 'ABORTED':
            pass
        #---DONE---
        elif self.state == 'DONE':
            pass
        #---RAID---
        elif self.state == 'RAID':
            if event == 'raid-done' :
                self.state = 'BLOCK'
                self.doRestoreBlock(arg)
        #---BLOCK---
        elif self.state == 'BLOCK':
            if event == 'block-restored' and not self.isBlockValid(arg) :
                self.state = 'FAILED'
                self.doDeleteAllRequests(arg)
                self.doRemoveTempFile(arg)
                self.doCloseFile(arg)
                self.doReportFailed(arg)
                self.doDestroyMe(arg)
            elif event == 'block-restored' and self.isBlockValid(arg) and not self.isLastBlock(arg) :
                self.state = 'RUN'
                self.doWriteRestoredData(arg)
                self.doDeleteBlockRequests(arg)
                self.doRemoveTempFile(arg)
            elif event == 'block-restored' and self.isBlockValid(arg) and self.isLastBlock(arg) :
                self.state = 'DONE'
                self.doWriteRestoredData(arg)
                self.doDeleteAllRequests(arg)
                self.doRemoveTempFile(arg)
                self.doCloseFile(arg)
                self.doReportDone(arg)
                self.doDestroyMe(arg)
        #---REQUEST---
        elif self.state == 'REQUEST':
            if ( event == 'timer-1sec' or event == 'request-done' ) and not self.isAborted(arg) and self.isBlockFixable(arg) :
                self.state = 'RAID'
                self.doPausePacketsQueue(arg)
                self.doReadRaid(arg)
            elif event == 'timer-5sec' and not self.isAborted(arg) and self.isTimePassed(arg) :
                self.doScanExistingPackets(arg)
                self.doRequestPackets(arg)
            elif event == 'timer-1sec' and self.isAborted(arg) :
                self.state = 'ABORTED'
                self.doPausePacketsQueue(arg)
                self.doDeleteAllRequests(arg)
                self.doCloseFile(arg)
                self.doReportAborted(arg)
                self.doDestroyMe(arg)
            elif event == 'packet-came-in' and self.isPacketValid(arg) and self.isCurrentBlock(arg) :
                self.doSavePacket(arg)
        #---RUN---
        elif self.state == 'RUN':
            if event == 'timer-01sec' and self.isAborted(arg) :
                self.state = 'ABORTED'
                self.doDeleteAllRequests(arg)
                self.doCloseFile(arg)
                self.doReportAborted(arg)
                self.doDestroyMe(arg)
            elif event == 'timer-01sec' and not self.isAborted(arg) :
                self.state = 'REQUEST'
                self.doStartNewBlock(arg)
                self.doReadPacketsQueue(arg)
                self.doScanExistingPackets(arg)
                self.doRequestPackets(arg)
        #---FAILED---
        elif self.state == 'FAILED':
            pass


    def isLastBlock(self, arg):
        """
        Condition method.
        """

    def isPacketValid(self, arg):
        """
        Condition method.
        """

    def isTimePassed(self, arg):
        """
        Condition method.
        """

    def isBlockFixable(self, arg):
        """
        Condition method.
        """

    def isCurrentBlock(self, arg):
        """
        Condition method.
        """

    def isAborted(self, arg):
        """
        Condition method.
        """

    def isBlockValid(self, arg):
        """
        Condition method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _Restore
        del _Restore
        _Restore = None

    def doCloseFile(self, arg):
        """
        Action method.
        """

    def doRestoreBlock(self, arg):
        """
        Action method.
        """

    def doScanExistingPackets(self, arg):
        """
        Action method.
        """

    def doDeleteBlockRequests(self, arg):
        """
        Action method.
        """

    def doRequestPackets(self, arg):
        """
        Action method.
        """

    def doRemoveTempFile(self, arg):
        """
        Action method.
        """

    def doSavePacket(self, arg):
        """
        Action method.
        """

    def doReadPacketsQueue(self, arg):
        """
        Action method.
        """

    def doDeleteAllRequests(self, arg):
        """
        Action method.
        """

    def doReadRaid(self, arg):
        """
        Action method.
        """

    def doPausePacketsQueue(self, arg):
        """
        Action method.
        """

    def doReportDone(self, arg):
        """
        Action method.
        """

    def doReportAborted(self, arg):
        """
        Action method.
        """

    def doReportFailed(self, arg):
        """
        Action method.
        """

    def doWriteRestoredData(self, arg):
        """
        Action method.
        """

    def doStartNewBlock(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

