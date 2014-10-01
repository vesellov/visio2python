

"""
.. module:: id_restorer
.. role:: red

BitPie.NET id_restorer() Automat

.. raw:: html

    <a href="id_restorer.png" target="_blank">
    <img src="id_restorer.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`my-id-failed`
    * :red:`my-id-received`
    * :red:`restore-failed`
    * :red:`restore-success`
    * :red:`start`
"""

import automat

_IdRestorer = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _IdRestorer
    if _IdRestorer is None:
        # set automat name and starting state here
        _IdRestorer = IdRestorer('id_restorer', 'VERIFY')
    if event is not None:
        _IdRestorer.automat(event, arg)
    return _IdRestorer


class IdRestorer(automat.Automat):
    """
    This class implements all the functionality of the ``id_restorer()`` state machine.
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
        #---VERIFY---
        if self.state == 'VERIFY':
            if event == 'restore-failed' :
                self.state = 'FAILED'
                self.doPrint(arg)
                self.doClearWorkingIDURL(arg)
                self.doClearWorkingKey(arg)
                self.doDestroyMe(arg)
            elif event == 'restore-success' :
                self.state = 'RESTORED!'
                self.doPrint(self.msg('MSG_06', arg))
                self.doRestoreSave(arg)
                self.doDestroyMe(arg)
        #---MY_ID---
        elif self.state == 'MY_ID':
            if event == 'my-id-failed' :
                self.state = 'FAILED'
                self.doPrint(self.msg('MSG_04', arg))
                self.doClearWorkingIDURL(arg)
                self.doClearWorkingKey(arg)
                self.doDestroyMe(arg)
            elif event == 'my-id-received' :
                self.state = 'VERIFY'
                self.doPrint(self.msg('MSG_05', arg))
                self.doVerifyAndRestore(arg)
        #---AT_STARTUP---
        elif self.state == 'AT_STARTUP':
            if event == 'start' :
                self.state = 'MY_ID'
                self.doPrint(self.msg('MSG_01', arg))
                self.doSetWorkingIDURL(arg)
                self.doSetWorkingKey(arg)
                self.doRequestMyIdentity(arg)
        #---RESTORED!---
        elif self.state == 'RESTORED!':
            pass
        #---FAILED---
        elif self.state == 'FAILED':
            pass


    def doPrint(self, arg):
        """
        Action method.
        """

    def doRequestMyIdentity(self, arg):
        """
        Action method.
        """

    def doRestoreSave(self, arg):
        """
        Action method.
        """

    def doSetWorkingKey(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _IdRestorer
        del _IdRestorer
        _IdRestorer = None

    def doClearWorkingKey(self, arg):
        """
        Action method.
        """

    def doClearWorkingIDURL(self, arg):
        """
        Action method.
        """

    def doVerifyAndRestore(self, arg):
        """
        Action method.
        """

    def doSetWorkingIDURL(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

