

"""
.. module:: backup_rebuilder
.. role:: red

BitPie.NET backup_rebuilder() Automat

.. raw:: html

    <a href="backup_rebuilder.png" target="_blank">
    <img src="backup_rebuilder.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`backup-ready`
    * :red:`inbox-data-packet`
    * :red:`init`
    * :red:`rebuilding-finished`
    * :red:`requests-sent`
    * :red:`start`
    * :red:`timer-10sec`
    * :red:`timer-1min`
    * :red:`timer-1sec`
"""

import automat

_BackupRebuilder = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _BackupRebuilder
    if _BackupRebuilder is None:
        # set automat name and starting state here
        _BackupRebuilder = BackupRebuilder('backup_rebuilder', 'REQUEST')
    if event is not None:
        _BackupRebuilder.automat(event, arg)
    return _BackupRebuilder


class BackupRebuilder(automat.Automat):
    """
    This class implements all the functionality of the ``backup_rebuilder()`` state machine.
    """

    timers = {
        'timer-1min': (60, ['REQUEST']),
        'timer-1sec': (1.0, ['REQUEST','NEXT_BACKUP']),
        'timer-10sec': (10.0, ['REQUEST']),
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
        #---REQUEST---
        if self.state == 'REQUEST':
            if ( event == 'timer-10sec' or event == 'inbox-data-packet' or event == 'requests-sent' ) and self.isChanceToRebuild(arg) :
                self.state = 'REBUILDING'
                self.doAttemptRebuild(arg)
            elif event == 'timer-1min' or ( event == 'requests-sent' and self.isRequestQueueEmpty(arg) and not self.isMissingPackets(arg) ) :
                self.state = 'DONE'
            elif event == 'timer-1sec' and self.isStopped(arg) :
                self.state = 'STOPPED'
        #---STOPPED---
        elif self.state == 'STOPPED':
            if event == 'init' :
                pass
            elif event == 'start' :
                self.state = 'NEXT_BACKUP'
                self.doClearStoppedFlag(arg)
        #---NEXT_BACKUP---
        elif self.state == 'NEXT_BACKUP':
            if event == 'timer-1sec' and not self.isStopped(arg) and self.isMoreBackups(arg) :
                self.state = 'PREPARE'
                self.doPrepareNextBackup(arg)
            elif event == 'timer-1sec' and not self.isMoreBackups(arg) and not self.isStopped(arg) :
                self.state = 'DONE'
            elif event == 'timer-1sec' and self.isStopped(arg) :
                self.state = 'STOPPED'
        #---DONE---
        elif self.state == 'DONE':
            if event == 'start' :
                self.state = 'NEXT_BACKUP'
                self.doClearStoppedFlag(arg)
        #---PREPARE---
        elif self.state == 'PREPARE':
            if event == 'backup-ready' and self.isStopped(arg) :
                self.state = 'STOPPED'
            elif event == 'backup-ready' and not self.isStopped(arg) and self.isMoreBlocks(arg) :
                self.state = 'REQUEST'
                self.doRequestAvailableBlocks(arg)
            elif event == 'backup-ready' and not self.isStopped(arg) and not self.isMoreBlocks(arg) and self.isMoreBackups(arg) :
                self.state = 'NEXT_BACKUP'
            elif event == 'backup-ready' and ( not self.isMoreBackups(arg) and not self.isMoreBlocks(arg) ) :
                self.state = 'DONE'
        #---REBUILDING---
        elif self.state == 'REBUILDING':
            if event == 'rebuilding-finished' and self.isStopped(arg) :
                self.state = 'STOPPED'
            elif event == 'rebuilding-finished' and not self.isStopped(arg) and self.isMoreBlocks(arg) :
                self.state = 'REQUEST'
                self.doRequestAvailableBlocks(arg)
            elif event == 'rebuilding-finished' and not self.isStopped(arg) and not self.isMoreBlocks(arg) :
                self.state = 'PREPARE'
                self.doPrepareNextBackup(arg)


    def isMoreBackups(self, arg):
        """
        Condition method.
        """

    def isChanceToRebuild(self, arg):
        """
        Condition method.
        """

    def isRequestQueueEmpty(self, arg):
        """
        Condition method.
        """

    def isMissingPackets(self, arg):
        """
        Condition method.
        """

    def isMoreBlocks(self, arg):
        """
        Condition method.
        """

    def isStopped(self, arg):
        """
        Condition method.
        """

    def doRequestAvailableBlocks(self, arg):
        """
        Action method.
        """

    def doAttemptRebuild(self, arg):
        """
        Action method.
        """

    def doPrepareNextBackup(self, arg):
        """
        Action method.
        """

    def doClearStoppedFlag(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

