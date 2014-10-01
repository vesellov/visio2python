

"""
.. module:: fire_hire
.. role:: red

BitPie.NET fire_hire() Automat

.. raw:: html

    <a href="fire_hire.png" target="_blank">
    <img src="fire_hire.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`init`
    * :red:`instant`
    * :red:`made-decision`
    * :red:`restart`
    * :red:`search-failed`
    * :red:`supplier-connected`
    * :red:`supplier-state-changed`
    * :red:`timer-15sec`
"""

import automat

_FireHire = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _FireHire
    if _FireHire is None:
        # set automat name and starting state here
        _FireHire = FireHire('fire_hire', 'READY')
    if event is not None:
        _FireHire.automat(event, arg)
    return _FireHire


class FireHire(automat.Automat):
    """
    This class implements all the functionality of the ``fire_hire()`` state machine.
    """

    timers = {
        'timer-15sec': (15.0, ['FIRE_MANY','SUPPLIERS?']),
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
        #---READY---
        if self.state == 'READY':
            if ( event == 'restart' or ( event == 'instant' and self.NeedRestart ) ) and self.isConfigChanged(arg) and self.isExistSomeSuppliers(arg) :
                self.state = 'SUPPLIERS?'
                self.NeedRestart=False
                self.doSaveConfig(arg)
                self.doConnectSuppliers(arg)
            elif ( event == 'restart' or ( event == 'instant' and self.NeedRestart ) ) and not ( self.isConfigChanged(arg) and self.isExistSomeSuppliers(arg) ) :
                self.state = 'DECISION?'
                self.NeedRestart=False
                self.doDecideToDismiss(arg)
        #---FIRE_MANY---
        elif self.state == 'FIRE_MANY':
            if event == 'timer-15sec' :
                self.state = 'READY'
                self.doCloseConnectors(arg)
                self.doClearDismissList(arg)
                backup_monitor.A('suppliers-changed')
            elif event == 'supplier-state-changed' and not self.isAllDismissed(arg) :
                self.doCloseConnector(arg)
            elif event == 'restart' :
                self.NeedRestart=True
            elif event == 'supplier-state-changed' and self.isAllDismissed(arg) :
                self.state = 'READY'
                self.doCloseConnector(arg)
                self.doClearDismissList(arg)
                backup_monitor.A('suppliers-changed')
        #---DECISION?---
        elif self.state == 'DECISION?':
            if event == 'made-decision' and not self.isMoreNeeded(arg) and not self.isSomeoneToDismiss(arg) :
                self.state = 'READY'
                backup_monitor.A('fire-hire-finished')
            elif event == 'made-decision' and self.isMoreNeeded(arg) :
                self.state = 'HIRE_ONE'
                self.doRememberSuppliers(arg)
                supplier_finder.A('start')
            elif event == 'made-decision' and self.isSomeoneToDismiss(arg) and not self.isMoreNeeded(arg) :
                self.state = 'FIRE_MANY'
                self.doRememberSuppliers(arg)
                self.doRemoveSuppliers(arg)
                self.doDisconnectSuppliers(arg)
            elif event == 'restart' :
                self.NeedRestart=True
        #---HIRE_ONE---
        elif self.state == 'HIRE_ONE':
            if event == 'search-failed' and self.isSomeoneToDismiss(arg) :
                self.state = 'FIRE_MANY'
                self.doDisconnectSuppliers(arg)
                self.doRemoveSuppliers(arg)
                self.doScheduleNextRestart(arg)
            elif event == 'supplier-connected' and not self.isStillNeeded(arg) and self.isSomeoneToDismiss(arg) :
                self.state = 'FIRE_MANY'
                self.doSubstituteSupplier(arg)
                self.doDisconnectSuppliers(arg)
            elif event == 'restart' :
                self.NeedRestart=True
            elif event == 'supplier-connected' and not self.isStillNeeded(arg) and not self.isSomeoneToDismiss(arg) :
                self.state = 'READY'
                self.doSubstituteSupplier(arg)
                backup_monitor.A('suppliers-changed')
            elif event == 'search-failed' and not self.isSomeoneToDismiss(arg) :
                self.state = 'READY'
                self.doScheduleNextRestart(arg)
                backup_monitor.A('suppliers-changed')
            elif event == 'supplier-connected' and self.isStillNeeded(arg) :
                self.doSubstituteSupplier(arg)
                supplier_finder.A('start')
        #---SUPPLIERS?---
        elif self.state == 'SUPPLIERS?':
            if ( event == 'supplier-state-changed' and self.isAllReady(arg) ) or event == 'timer-15sec' :
                self.state = 'DECISION?'
                self.doDecideToDismiss(arg)
            elif event == 'restart' :
                self.NeedRestart=True
        #---AT_STARTUP---
        elif self.state == 'AT_STARTUP':
            if event == 'init' :
                self.state = 'READY'
                self.NeedRestart=False


    def isAllDismissed(self, arg):
        """
        Condition method.
        """

    def isSomeoneToDismiss(self, arg):
        """
        Condition method.
        """

    def isExistSomeSuppliers(self, arg):
        """
        Condition method.
        """

    def isMoreNeeded(self, arg):
        """
        Condition method.
        """

    def isStillNeeded(self, arg):
        """
        Condition method.
        """

    def isConfigChanged(self, arg):
        """
        Condition method.
        """

    def isAllReady(self, arg):
        """
        Condition method.
        """

    def doDecideToDismiss(self, arg):
        """
        Action method.
        """

    def doSaveConfig(self, arg):
        """
        Action method.
        """

    def doRemoveSuppliers(self, arg):
        """
        Action method.
        """

    def doClearDismissList(self, arg):
        """
        Action method.
        """

    def doDisconnectSuppliers(self, arg):
        """
        Action method.
        """

    def doCloseConnector(self, arg):
        """
        Action method.
        """

    def doRememberSuppliers(self, arg):
        """
        Action method.
        """

    def doSubstituteSupplier(self, arg):
        """
        Action method.
        """

    def doConnectSuppliers(self, arg):
        """
        Action method.
        """

    def doCloseConnectors(self, arg):
        """
        Action method.
        """

    def doScheduleNextRestart(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

