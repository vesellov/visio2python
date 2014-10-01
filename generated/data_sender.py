

"""
.. module:: data_sender
.. role:: red

BitPie.NET data_sender() Automat

.. raw:: html

    <a href="data_sender.png" target="_blank">
    <img src="data_sender.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`block-acked`
    * :red:`block-failed`
    * :red:`init`
    * :red:`new-data`
    * :red:`restart`
    * :red:`scan-done`
    * :red:`timer-1min`
    * :red:`timer-1sec`
"""

import automat

_DataSender = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _DataSender
    if _DataSender is None:
        # set automat name and starting state here
        _DataSender = DataSender('data_sender', 'READY')
    if event is not None:
        _DataSender.automat(event, arg)
    return _DataSender


class DataSender(automat.Automat):
    """
    This class implements all the functionality of the ``data_sender()`` state machine.
    """

    timers = {
        'timer-1min': (60, ['READY']),
        'timer-1sec': (1.0, ['SENDING']),
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
            if event == 'init' :
                pass
            elif event == 'new-data' or event == 'timer-1min' or event == 'restart' :
                self.state = 'SCAN_BLOCKS'
                self.doScanAndQueue(arg)
        #---SENDING---
        elif self.state == 'SENDING':
            if event == 'timer-1sec' :
                self.doPrintStats(arg)
            elif event == 'restart' or ( ( event == 'timer-1sec' or event == 'block-acked' or event == 'block-failed' ) and self.isQueueEmpty(arg) ) :
                self.state = 'SCAN_BLOCKS'
                self.doScanAndQueue(arg)
        #---SCAN_BLOCKS---
        elif self.state == 'SCAN_BLOCKS':
            if event == 'scan-done' and self.isQueueEmpty(arg) :
                self.state = 'READY'
                self.doRemoveUnusedFiles(arg)
            elif event == 'scan-done' and not self.isQueueEmpty(arg) :
                self.state = 'SENDING'


    def isQueueEmpty(self, arg):
        """
        Condition method.
        """

    def doScanAndQueue(self, arg):
        """
        Action method.
        """

    def doRemoveUnusedFiles(self, arg):
        """
        Action method.
        """

    def doPrintStats(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

