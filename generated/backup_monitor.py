

"""
.. module:: backup_monitor
.. role:: red

BitPie.NET backup_monitor() Automat

.. raw:: html

    <a href="backup_monitor.png" target="_blank">
    <img src="backup_monitor.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`backup_rebuilder.state`
    * :red:`fire-hire-finished`
    * :red:`init`
    * :red:`instant`
    * :red:`list-backups-done`
    * :red:`list_files_orator.state`
    * :red:`restart`
    * :red:`suppliers-changed`
"""

import automat

_BackupMonitor = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _BackupMonitor
    if _BackupMonitor is None:
        # set automat name and starting state here
        _BackupMonitor = BackupMonitor('backup_monitor', 'LIST_FILES')
    if event is not None:
        _BackupMonitor.automat(event, arg)
    return _BackupMonitor


class BackupMonitor(automat.Automat):
    """
    This class implements all the functionality of the ``backup_monitor()`` state machine.
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
        #---LIST_FILES---
        if self.state == 'LIST_FILES':
            if ( event == 'list_files_orator.state' and arg == 'SAW_FILES' ) :
                self.state = 'LIST_BACKUPS'
                backup_db_keeper.A('restart')
                data_sender.A('restart')
                self.doPrepareListBackups(arg)
            elif ( event == 'list_files_orator.state' and arg == 'NO_FILES' ) :
                self.state = 'READY'
            elif event == 'restart' :
                self.RestartAgain=True
        #---LIST_BACKUPS---
        elif self.state == 'LIST_BACKUPS':
            if event == 'restart' :
                self.state = 'FIRE_HIRE'
                fire_hire.A('restart')
            elif event == 'list-backups-done' :
                self.state = 'REBUILDING'
                backup_rebuilder.A('start')
            elif event == 'restart' :
                self.RestartAgain=True
        #---REBUILDING---
        elif self.state == 'REBUILDING':
            if event == 'restart' :
                self.state = 'FIRE_HIRE'
                backup_rebuilder.SetStoppedFlag()
                fire_hire.A('restart')
            elif ( event == 'backup_rebuilder.state' and arg in [ 'DONE' , 'STOPPED' ] ) :
                self.state = 'READY'
                self.doCleanUpBackups(arg)
        #---FIRE_HIRE---
        elif self.state == 'FIRE_HIRE':
            if event == 'suppliers-changed' and self.isSuppliersNumberChanged(arg) :
                self.state = 'LIST_FILES'
                self.doDeleteAllBackups(arg)
                self.doRememberSuppliers(arg)
                list_files_orator.A('need-files')
            elif event == 'restart' :
                self.RestartAgain=True
            elif event == 'fire-hire-finished' :
                self.state = 'LIST_FILES'
                list_files_orator.A('need-files')
            elif event == 'suppliers-changed' and not self.isSuppliersNumberChanged(arg) :
                self.state = 'LIST_FILES'
                self.doUpdateSuppliers(arg)
                self.doRememberSuppliers(arg)
                list_files_orator.A('need-files')
        #---READY---
        elif self.state == 'READY':
            if event == 'init' :
                self.RestartAgain=False
                self.doSuppliersInit(arg)
                backup_rebuilder.A('init')
            elif event == 'restart' or ( event == 'instant' and self.RestartAgain ) :
                self.state = 'FIRE_HIRE'
                self.RestartAgain=False
                self.doRememberSuppliers(arg)
                fire_hire.A('restart')


    def isSuppliersNumberChanged(self, arg):
        """
        Condition method.
        """

    def doCleanUpBackups(self, arg):
        """
        Action method.
        """

    def doSuppliersInit(self, arg):
        """
        Action method.
        """

    def doDeleteAllBackups(self, arg):
        """
        Action method.
        """

    def doRememberSuppliers(self, arg):
        """
        Action method.
        """

    def doPrepareListBackups(self, arg):
        """
        Action method.
        """

    def doUpdateSuppliers(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

