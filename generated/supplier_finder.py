

"""
.. module:: supplier_finder
.. role:: red

BitPie.NET supplier_finder() Automat

.. raw:: html

    <a href="supplier_finder.png" target="_blank">
    <img src="supplier_finder.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`found-one-user`
    * :red:`inbox-packet`
    * :red:`start`
    * :red:`supplier-connected`
    * :red:`supplier-not-connected`
    * :red:`timer-10sec`
    * :red:`users-not-found`
"""

import automat

_SupplierFinder = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _SupplierFinder
    if _SupplierFinder is None:
        # set automat name and starting state here
        _SupplierFinder = SupplierFinder('supplier_finder', 'ACK?')
    if event is not None:
        _SupplierFinder.automat(event, arg)
    return _SupplierFinder


class SupplierFinder(automat.Automat):
    """
    This class implements all the functionality of the ``supplier_finder()`` state machine.
    """

    timers = {
        'timer-10sec': (10.0, ['ACK?','SERVICE?']),
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
        #---ACK?---
        if self.state == 'ACK?':
            if event == 'inbox-packet' and self.isAckFromUser(arg) :
                self.state = 'SERVICE?'
                self.doSupplierConnect(arg)
            elif self.Attempts==5 and event == 'timer-10sec' :
                self.state = 'FAILED'
                self.doDestroyMe(arg)
                fire_hire.A('search-failed')
            elif event == 'timer-10sec' and self.Attempts<5 :
                self.state = 'RANDOM_USER'
                self.doDHTFindRandomUser(arg)
        #---AT_STARTUP---
        elif self.state == 'AT_STARTUP':
            if event == 'start' :
                self.state = 'RANDOM_USER'
                self.Attempts=0
                self.doInit(arg)
                self.doDHTFindRandomUser(arg)
        #---RANDOM_USER---
        elif self.state == 'RANDOM_USER':
            if event == 'users-not-found' :
                self.state = 'FAILED'
                self.doDestroyMe(arg)
                fire_hire.A('search-failed')
            elif event == 'found-one-user' :
                self.state = 'ACK?'
                self.doCleanPrevUser(arg)
                self.doRememberUser(arg)
                self.Attempts+=1
                self.doSendMyIdentity(arg)
        #---FAILED---
        elif self.state == 'FAILED':
            pass
        #---SERVICE?---
        elif self.state == 'SERVICE?':
            if event == 'timer-10sec' and self.Attempts<5 :
                self.state = 'RANDOM_USER'
                self.doDHTFindRandomUser(arg)
            elif self.Attempts==5 and ( event == 'timer-10sec' or event == 'supplier-not-connected' ) :
                self.state = 'FAILED'
                self.doDestroyMe(arg)
                fire_hire.A('search-failed')
            elif event == 'supplier-connected' :
                self.state = 'DONE'
                fire_hire.A('supplier-connected', self.target_idurl)
                self.doDestroyMe(arg)
            elif self.Attempts<5 and event == 'supplier-not-connected' :
                self.state = 'RANDOM_USER'
                self.doDHTFindRandomUser(arg)
        #---DONE---
        elif self.state == 'DONE':
            pass


    def isAckFromUser(self, arg):
        """
        Condition method.
        """

    def doSendMyIdentity(self, arg):
        """
        Action method.
        """

    def doCleanPrevUser(self, arg):
        """
        Action method.
        """

    def doDHTFindRandomUser(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _SupplierFinder
        del _SupplierFinder
        _SupplierFinder = None

    def doRememberUser(self, arg):
        """
        Action method.
        """

    def doInit(self, arg):
        """
        Action method.
        """

    def doSupplierConnect(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

