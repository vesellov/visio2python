

"""
.. module:: initializer
.. role:: red

BitPie.NET initializer() Automat

.. raw:: html

    <a href="initializer.png" target="_blank">
    <img src="initializer.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`init-contacts-done`
    * :red:`init-local-done`
    * :red:`init-modules-done`
    * :red:`installer.state`
    * :red:`p2p_connector.state`
    * :red:`run`
    * :red:`run-cmd-line-recover`
    * :red:`run-cmd-line-register`
    * :red:`shutdowner.state`
"""

import automat

_Initializer = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _Initializer
    if _Initializer is None:
        # set automat name and starting state here
        _Initializer = Initializer('initializer', 'AT_STARTUP')
    if event is not None:
        _Initializer.automat(event, arg)
    return _Initializer


class Initializer(automat.Automat):
    """
    This class implements all the functionality of the ``initializer()`` state machine.
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
            if event == 'run-cmd-line-register' :
                self.state = 'INSTALL'
                self.flagCmdLine=True
                installer.A('register-cmd-line', arg)
                shutdowner.A('init')
                shutdowner.A('ready')
            elif event == 'run' :
                self.state = 'LOCAL'
                self.doInitLocal(arg)
                self.flagCmdLine=False
                shutdowner.A('init')
            elif event == 'run-cmd-line-recover' :
                self.state = 'INSTALL'
                self.flagCmdLine=True
                installer.A('recover-cmd-line', arg)
                shutdowner.A('init')
                shutdowner.A('ready')
        #---LOCAL---
        elif self.state == 'LOCAL':
            if event == 'init-local-done' and not self.isInstalled(arg) and not self.isGUIPossible(arg) :
                self.state = 'STOPPING'
                self.doPrintMessage(arg)
                shutdowner.A('ready')
                shutdowner.A('stop', "exit")
            elif event == 'init-local-done' and not self.isInstalled(arg) and self.isGUIPossible(arg) :
                self.state = 'INSTALL'
                self.doShowGUI(arg)
                installer.A('init')
                self.doUpdate(arg)
                shutdowner.A('ready')
            elif event == 'init-local-done' and self.isInstalled(arg) :
                self.state = 'CONTACTS'
                self.doShowGUI(arg)
                self.doInitContacts(arg)
        #---INSTALL---
        elif self.state == 'INSTALL':
            if not self.flagCmdLine and ( event == 'installer.state' and arg == 'DONE' ) :
                self.state = 'STOPPING'
                shutdowner.A('stop', "restartnshow")
            elif self.flagCmdLine and ( event == 'installer.state' and arg == 'DONE' ) :
                self.state = 'STOPPING'
                shutdowner.A('stop', "exit")
            elif ( event == 'shutdowner.state' and arg == 'FINISHED' ) :
                self.state = 'EXIT'
                self.doDestroyMe(arg)
        #---CONTACTS---
        elif self.state == 'CONTACTS':
            if event == 'init-contacts-done' :
                self.state = 'CONNECTION'
                self.doInitConnection(arg)
                p2p_connector.A('init')
                self.doUpdate(arg)
                shutdowner.A('ready')
            elif ( event == 'shutdowner.state' and arg == 'FINISHED' ) :
                self.state = 'EXIT'
                self.doDestroyMe(arg)
        #---CONNECTION---
        elif self.state == 'CONNECTION':
            if ( event == 'shutdowner.state' and arg == 'FINISHED' ) :
                self.state = 'EXIT'
                self.doDestroyMe(arg)
            elif ( event == 'p2p_connector.state' and arg in [ 'CONNECTED' , 'DISCONNECTED' ] ) :
                self.state = 'MODULES'
                self.doInitModules(arg)
                self.doUpdate(arg)
        #---MODULES---
        elif self.state == 'MODULES':
            if event == 'init-modules-done' :
                self.state = 'READY'
                self.doUpdate(arg)
            elif ( event == 'shutdowner.state' and arg == 'FINISHED' ) :
                self.state = 'EXIT'
                self.doDestroyMe(arg)
        #---READY---
        elif self.state == 'READY':
            if ( event == 'shutdowner.state' and arg == 'FINISHED' ) :
                self.state = 'EXIT'
                self.doDestroyMe(arg)
        #---EXIT---
        elif self.state == 'EXIT':
            pass
        #---STOPPING---
        elif self.state == 'STOPPING':
            if ( event == 'shutdowner.state' and arg == 'FINISHED' ) :
                self.state = 'EXIT'
                self.doUpdate(arg)
                self.doDestroyMe(arg)


    def isGUIPossible(self, arg):
        """
        Condition method.
        """

    def isInstalled(self, arg):
        """
        Condition method.
        """

    def doInitLocal(self, arg):
        """
        Action method.
        """

    def doPrintMessage(self, arg):
        """
        Action method.
        """

    def doShowGUI(self, arg):
        """
        Action method.
        """

    def doInitConnection(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _Initializer
        del _Initializer
        _Initializer = None

    def doUpdate(self, arg):
        """
        Action method.
        """

    def doInitModules(self, arg):
        """
        Action method.
        """

    def doInitContacts(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

