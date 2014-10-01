

"""
.. module:: supplier_connector
.. role:: red

BitPie.NET supplier_connector() Automat

.. raw:: html

    <a href="supplier_connector.png" target="_blank">
    <img src="supplier_connector.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`ack`
    * :red:`close`
    * :red:`connect`
    * :red:`disconnect`
    * :red:`fail`
    * :red:`shutdown`
    * :red:`timer-10sec`
    * :red:`timer-20sec`
"""

import automat

_SupplierConnector = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _SupplierConnector
    if _SupplierConnector is None:
        # set automat name and starting state here
        _SupplierConnector = SupplierConnector('supplier_connector', 'NO_SERVICE')
    if event is not None:
        _SupplierConnector.automat(event, arg)
    return _SupplierConnector


class SupplierConnector(automat.Automat):
    """
    This class implements all the functionality of the ``supplier_connector()`` state machine.
    """

    timers = {
        'timer-10sec': (10.0, ['REFUSE']),
        'timer-20sec': (20.0, ['REQUEST']),
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
        #---NO_SERVICE---
        if self.state == 'NO_SERVICE':
            if event == 'shutdown' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'ack' and self.isServiceAccepted(arg) :
                self.state = 'CONNECTED'
                self.doReportConnect(arg)
            elif event == 'connect' :
                self.state = 'REQUEST'
                self.doRequestService(arg)
                self.GoDisconnect=False
            elif event == 'disconnect' :
                self.doReportNoService(arg)
        #---CONNECTED---
        elif self.state == 'CONNECTED':
            if event == 'close' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'fail' or event == 'connect' :
                self.state = 'REQUEST'
                self.doRequestService(arg)
                self.GoDisconnect=False
            elif event == 'disconnect' :
                self.state = 'REFUSE'
                self.doCancelService(arg)
        #---CLOSED---
        elif self.state == 'CLOSED':
            pass
        #---DISCONNECTED---
        elif self.state == 'DISCONNECTED':
            if event == 'connect' :
                self.state = 'REQUEST'
                self.doRequestService(arg)
                self.GoDisconnect=False
            elif event == 'shutdown' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'ack' and self.isServiceAccepted(arg) :
                self.state = 'CONNECTED'
                self.doReportConnect(arg)
            elif event == 'fail' :
                self.state = 'NO_SERVICE'
                self.doReportNoService(arg)
            elif event == 'disconnect' :
                self.state = 'REFUSE'
                self.doCancelService(arg)
        #---REQUEST---
        elif self.state == 'REQUEST':
            if event == 'fail' or ( event == 'ack' and not self.isServiceAccepted(arg) and not self.GoDisconnect ) :
                self.state = 'NO_SERVICE'
                self.doReportNoService(arg)
            elif event == 'timer-20sec' :
                self.state = 'DISCONNECTED'
                self.doCleanRequest(arg)
                self.doReportDisconnect(arg)
            elif event == 'disconnect' :
                self.GoDisconnect=True
            elif event == 'shutdown' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif self.GoDisconnect and event == 'ack' and self.isServiceAccepted(arg) :
                self.state = 'REFUSE'
                self.doCancelService(arg)
            elif event == 'ack' and not self.GoDisconnect and self.isServiceAccepted(arg) :
                self.state = 'CONNECTED'
                self.doReportConnect(arg)
        #---REFUSE---
        elif self.state == 'REFUSE':
            if event == 'shutdown' :
                self.state = 'CLOSED'
                self.doCleanRequest(arg)
                self.doDestroyMe(arg)
            elif event == 'timer-10sec' or event == 'fail' or ( event == 'ack' and self.isServiceCancelled(arg) ) :
                self.state = 'NO_SERVICE'
                self.doCleanRequest(arg)
                self.doReportNoService(arg)


    def isServiceAccepted(self, arg):
        """
        Condition method.
        """

    def isServiceCancelled(self, arg):
        """
        Condition method.
        """

    def doReportNoService(self, arg):
        """
        Action method.
        """

    def doCleanRequest(self, arg):
        """
        Action method.
        """

    def doReportDisconnect(self, arg):
        """
        Action method.
        """

    def doCancelService(self, arg):
        """
        Action method.
        """

    def doRequestService(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _SupplierConnector
        del _SupplierConnector
        _SupplierConnector = None

    def doReportConnect(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

