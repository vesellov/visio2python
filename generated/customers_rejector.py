

"""
.. module:: customers_rejector
.. role:: red

BitPie.NET customers_rejector() Automat

.. raw:: html

    <a href="customers_rejector.png" target="_blank">
    <img src="customers_rejector.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`packets-sent`
    * :red:`restart`
    * :red:`space-enough`
    * :red:`space-overflow`
"""

import automat

_CustomersRejector = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _CustomersRejector
    if _CustomersRejector is None:
        # set automat name and starting state here
        _CustomersRejector = CustomersRejector('customers_rejector', 'READY')
    if event is not None:
        _CustomersRejector.automat(event, arg)
    return _CustomersRejector


class CustomersRejector(automat.Automat):
    """
    This class implements all the functionality of the ``customers_rejector()`` state machine.
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
        #---READY---
        if self.state == 'READY':
            if event == 'restart' :
                self.state = 'CAPACITY?'
                self.doTestMyCapacity(arg)
        #---REJECT_GUYS---
        elif self.state == 'REJECT_GUYS':
            if event == 'packets-sent' :
                self.state = 'READY'
                self.doRestartLocalTester(arg)
            elif event == 'restart' :
                self.state = 'CAPACITY?'
                self.doTestMyCapacity(arg)
        #---CAPACITY?---
        elif self.state == 'CAPACITY?':
            if event == 'space-enough' :
                self.state = 'READY'
            elif event == 'space-overflow' :
                self.state = 'REJECT_GUYS'
                self.doRemoveCustomers(arg)
                self.doSendRejectService(arg)


    def doRemoveCustomers(self, arg):
        """
        Action method.
        """

    def doRestartLocalTester(self, arg):
        """
        Action method.
        """

    def doTestMyCapacity(self, arg):
        """
        Action method.
        """

    def doSendRejectService(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

