

"""
.. module:: shutdowner
.. role:: red

BitPie.NET shutdowner() Automat

.. raw:: html

    <a href="shutdowner.png" target="_blank">
    <img src="shutdowner.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`block`
    * :red:`init`
    * :red:`reactor-stopped`
    * :red:`ready`
    * :red:`stop`
    * :red:`unblock`
"""

import automat

_Shutdowner = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _Shutdowner
    if _Shutdowner is None:
        # set automat name and starting state here
        _Shutdowner = Shutdowner('shutdowner', 'AT_STARTUP')
    if event is not None:
        _Shutdowner.automat(event, arg)
    return _Shutdowner


class Shutdowner(automat.Automat):
    """
    This class implements all the functionality of the ``shutdowner()`` state machine.
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
        #---AT_STARTUP---
        if self.state == 'AT_STARTUP':
            if event == 'init' :
                self.state = 'INIT'
                self.flagApp=False
                self.flagReactor=False
        #---FINISHED---
        elif self.state == 'FINISHED':
            pass
        #---INIT---
        elif self.state == 'INIT':
            if event == 'ready' and self.flagReactor :
                self.state = 'FINISHED'
                self.doKillAutomats(arg)
            elif event == 'reactor-stopped' :
                self.flagReactor=True
            elif event == 'ready' and not self.flagReactor and self.flagApp :
                self.state = 'STOPPING'
                self.doShutdown(arg)
            elif event == 'ready' and not self.flagReactor and not self.flagApp :
                self.state = 'READY'
            elif event == 'stop' :
                self.doSaveParam(arg)
                self.flagApp=True
        #---READY---
        elif self.state == 'READY':
            if event == 'block' :
                self.state = 'BLOCKED'
            elif event == 'reactor-stopped' :
                self.state = 'FINISHED'
                self.doKillAutomats(arg)
            elif event == 'stop' :
                self.state = 'STOPPING'
                self.doShutdown(arg)
        #---BLOCKED---
        elif self.state == 'BLOCKED':
            if event == 'unblock' and self.flagReactor :
                self.state = 'FINISHED'
                self.doKillAutomats(arg)
            elif event == 'unblock' and not self.flagReactor and not self.flagApp :
                self.state = 'READY'
            elif event == 'reactor-stopped' :
                self.flagReactor=True
            elif event == 'unblock' and not self.flagReactor and self.flagApp :
                self.state = 'STOPPING'
                self.doShutdown(arg)
            elif event == 'stop' :
                self.doSaveParam(arg)
                self.flagApp=True
        #---STOPPING---
        elif self.state == 'STOPPING':
            if event == 'reactor-stopped' :
                self.state = 'FINISHED'
                self.doKillAutomats(arg)


    def doKillAutomats(self, arg):
        """
        Action method.
        """

    def doSaveParam(self, arg):
        """
        Action method.
        """

    def doShutdown(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

