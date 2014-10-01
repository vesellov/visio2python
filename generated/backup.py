

"""
.. module:: backup
.. role:: red

BitPie.NET backup() Automat

.. raw:: html

    <a href="backup.png" target="_blank">
    <img src="backup.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`block-encrypted`
    * :red:`block-raid-done`
    * :red:`block-raid-started`
    * :red:`read-success`
    * :red:`start`
    * :red:`timer-001sec`
    * :red:`timer-01sec`
"""

import automat

_Backup = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _Backup
    if _Backup is None:
        # set automat name and starting state here
        _Backup = Backup('backup', 'AT_STARTUP')
    if event is not None:
        _Backup.automat(event, arg)
    return _Backup


class Backup(automat.Automat):
    """
    This class implements all the functionality of the ``backup()`` state machine.
    """

    timers = {
        'timer-01sec': (0.1, ['RAID']),
        'timer-001sec': (0.01, ['READ']),
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
            if event == 'start' :
                self.state = 'READ'
                self.doInit(arg)
                self.doFirstBlock(arg)
        #---READ---
        elif self.state == 'READ':
            if ( event == 'read-success' or event == 'timer-001sec' ) and self.isAborted(arg) :
                self.state = 'ABORTED'
                self.doClose(arg)
                self.doReport(arg)
                self.doDestroyMe(arg)
            elif ( event == 'read-success' or event == 'timer-001sec' ) and not self.isAborted(arg) and self.isPipeReady(arg) and not self.isEOF(arg) and not self.isReadingNow(arg) and not self.isBlockReady(arg) :
                self.doRead(arg)
            elif event == 'read-success' and not self.isReadingNow(arg) and ( self.isBlockReady(arg) or self.isEOF(arg) ) :
                self.state = 'ENCRYPT'
                self.doEncryptBlock(arg)
            elif event == 'block-raid-done' :
                self.doPopBlock(arg)
                self.doBlockReport(arg)
                data_sender.A('new-data')
        #---ENCRYPT---
        elif self.state == 'ENCRYPT':
            if event == 'block-raid-done' :
                self.doPopBlock(arg)
                self.doBlockReport(arg)
                data_sender.A('new-data')
            elif event == 'block-encrypted' :
                self.state = 'RAID'
                self.doBlockPushAndRaid(arg)
        #---RAID---
        elif self.state == 'RAID':
            if ( event == 'timer-01sec' or event == 'block-raid-done' or event == 'block-raid-started' ) and self.isAborted(arg) :
                self.state = 'ABORTED'
                self.doClose(arg)
                self.doReport(arg)
                self.doDestroyMe(arg)
            elif event == 'block-raid-done' and not self.isMoreBlocks(arg) and not self.isAborted(arg) :
                self.state = 'DONE'
                self.doPopBlock(arg)
                self.doBlockReport(arg)
                data_sender.A('new-data')
                self.doClose(arg)
                self.doReport(arg)
                self.doDestroyMe(arg)
            elif event == 'block-raid-started' and not self.isEOF(arg) and not self.isAborted(arg) :
                self.state = 'READ'
                self.doNextBlock(arg)
                self.doRead(arg)
            elif event == 'block-raid-done' and self.isMoreBlocks(arg) and not self.isAborted(arg) :
                self.doPopBlock(arg)
                self.doBlockReport(arg)
                data_sender.A('new-data')
        #---DONE---
        elif self.state == 'DONE':
            pass
        #---ABORTED---
        elif self.state == 'ABORTED':
            pass


    def isPipeReady(self, arg):
        """
        Condition method.
        """

    def isEOF(self, arg):
        """
        Condition method.
        """

    def isReadingNow(self, arg):
        """
        Condition method.
        """

    def isMoreBlocks(self, arg):
        """
        Condition method.
        """

    def isBlockReady(self, arg):
        """
        Condition method.
        """

    def isAborted(self, arg):
        """
        Condition method.
        """

    def doBlockReport(self, arg):
        """
        Action method.
        """

    def doClose(self, arg):
        """
        Action method.
        """

    def doNextBlock(self, arg):
        """
        Action method.
        """

    def doBlockPushAndRaid(self, arg):
        """
        Action method.
        """

    def doReport(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _Backup
        del _Backup
        _Backup = None

    def doPopBlock(self, arg):
        """
        Action method.
        """

    def doFirstBlock(self, arg):
        """
        Action method.
        """

    def doInit(self, arg):
        """
        Action method.
        """

    def doRead(self, arg):
        """
        Action method.
        """

    def doEncryptBlock(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

