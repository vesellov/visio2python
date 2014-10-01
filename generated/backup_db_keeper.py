

"""
.. module:: backup_db_keeper
.. role:: red

BitPie.NET backup_db_keeper() Automat

.. raw:: html

    <a href="backup_db_keeper.png" target="_blank">
    <img src="backup_db_keeper.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`all-responded`
    * :red:`db-info-acked`
    * :red:`init`
    * :red:`restart`
    * :red:`timer-1hour`
    * :red:`timer-1sec`
    * :red:`timer-30sec`
"""

import automat

_BackupDbKeeper = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _BackupDbKeeper
    if _BackupDbKeeper is None:
        # set automat name and starting state here
        _BackupDbKeeper = BackupDbKeeper('backup_db_keeper', 'AT_STARTUP')
    if event is not None:
        _BackupDbKeeper.automat(event, arg)
    return _BackupDbKeeper


class BackupDbKeeper(automat.Automat):
    """
    This class implements all the functionality of the ``backup_db_keeper()`` state machine.
    """

    timers = {
        'timer-1hour': (3600, ['READY']),
        'timer-1sec': (1.0, ['RESTART']),
        'timer-30sec': (30.0, ['RESTART','REQUEST','SENDING']),
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
                self.state = 'READY'
            elif event == 'restart' :
                self.state = 'RESTART'
        #---RESTART---
        elif self.state == 'RESTART':
            if event == 'timer-1sec' and self.isTimePassed(arg) and p2p_connector.A().state is 'CONNECTED' :
                self.state = 'REQUEST'
                self.doSuppliersRequestDBInfo(arg)
                self.doRememberTime(arg)
            elif event == 'timer-30sec' :
                self.state = 'READY'
        #---REQUEST---
        elif self.state == 'REQUEST':
            if event == 'restart' :
                self.state = 'RESTART'
            elif event == 'all-responded' or event == 'timer-30sec' :
                self.state = 'SENDING'
                self.doSuppliersSendDBInfo(arg)
        #---SENDING---
        elif self.state == 'SENDING':
            if event == 'restart' :
                self.state = 'RESTART'
            elif event == 'db-info-acked' and self.isAllSuppliersAcked(arg) :
                self.state = 'READY'
                self.doSetSyncFlag(arg)
            elif event == 'timer-30sec' :
                self.state = 'READY'
            elif event == 'db-info-acked' and not self.isAllSuppliersAcked(arg) :
                self.doSetSyncFlag(arg)
        #---READY---
        elif self.state == 'READY':
            if event == 'timer-1hour' or event == 'restart' :
                self.state = 'RESTART'


    def isAllSuppliersAcked(self, arg):
        """
        Condition method.
        """

    def isTimePassed(self, arg):
        """
        Condition method.
        """

    def doSetSyncFlag(self, arg):
        """
        Action method.
        """

    def doRememberTime(self, arg):
        """
        Action method.
        """

    def doSuppliersSendDBInfo(self, arg):
        """
        Action method.
        """

    def doSuppliersRequestDBInfo(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

