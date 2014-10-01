

"""
.. module:: installer
.. role:: red

BitPie.NET installer() Automat

.. raw:: html

    <a href="installer.png" target="_blank">
    <img src="installer.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`back`
    * :red:`id_registrator.state`
    * :red:`id_restorer.state`
    * :red:`init`
    * :red:`install_wizard.state`
    * :red:`load-from-file`
    * :red:`next`
    * :red:`paste-from-clipboard`
    * :red:`print`
    * :red:`recover-cmd-line`
    * :red:`recover-selected`
    * :red:`register-cmd-line`
    * :red:`register-selected`
    * :red:`register-start`
    * :red:`restore-start`
"""

import automat

_Installer = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _Installer
    if _Installer is None:
        # set automat name and starting state here
        _Installer = Installer('installer', 'AT_STARTUP')
    if event is not None:
        _Installer.automat(event, arg)
    return _Installer


class Installer(automat.Automat):
    """
    This class implements all the functionality of the ``installer()`` state machine.
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
                self.state = 'WHAT_TO_DO?'
                self.flagCmdLine=False
            elif event == 'recover-cmd-line' :
                self.state = 'RECOVER'
                self.flagCmdLine=True
                self.doInit(arg)
                id_restorer.A('start', arg)
            elif event == 'register-cmd-line' :
                self.state = 'REGISTER'
                self.flagCmdLine=True
                self.doInit(arg)
                id_registrator.A('start', arg)
        #---WHAT_TO_DO?---
        elif self.state == 'WHAT_TO_DO?':
            if event == 'register-selected' :
                self.state = 'INPUT_NAME'
                self.doUpdate(arg)
            elif event == 'recover-selected' :
                self.state = 'LOAD_KEY'
                self.doUpdate(arg)
        #---INPUT_NAME---
        elif self.state == 'INPUT_NAME':
            if event == 'print' :
                self.doPrint(arg)
                self.doUpdate(arg)
            elif event == 'register-start' and self.isNameValid(arg) :
                self.state = 'REGISTER'
                self.doClearOutput(arg)
                id_registrator.A('start', arg)
                self.doUpdate(arg)
            elif event == 'back' :
                self.state = 'WHAT_TO_DO?'
                self.doClearOutput(arg)
                self.doUpdate(arg)
            elif event == 'register-start' and not self.isNameValid(arg) :
                self.doClearOutput(arg)
                self.doPrintIncorrectName(arg)
                self.doUpdate(arg)
        #---LOAD_KEY---
        elif self.state == 'LOAD_KEY':
            if event == 'print' :
                self.doPrint(arg)
                self.doUpdate(arg)
            elif event == 'paste-from-clipboard' :
                self.doPasteKey(arg)
                self.doUpdate(arg)
            elif event == 'back' :
                self.state = 'WHAT_TO_DO?'
                self.doClearOutput(arg)
                self.doUpdate(arg)
            elif event == 'load-from-file' :
                self.doReadKey(arg)
                self.doUpdate(arg)
            elif event == 'restore-start' :
                self.state = 'RECOVER'
                self.doClearOutput(arg)
                id_restorer.A('start', arg)
                self.doUpdate(arg)
        #---RECOVER---
        elif self.state == 'RECOVER':
            if event == 'print' :
                self.doPrint(arg)
                self.doUpdate(arg)
            elif ( event == 'id_restorer.state' and arg == 'FAILED' ) and not self.flagCmdLine :
                self.state = 'LOAD_KEY'
                self.doUpdate(arg)
            elif ( event == 'id_restorer.state' and arg == 'RESTORED!' ) or ( ( event == 'id_restorer.state' and arg == 'FAILED' ) and self.flagCmdLine ) :
                self.state = 'DONE'
                self.doUpdate(arg)
        #---DONE---
        elif self.state == 'DONE':
            if event == 'print' :
                self.doPrint(arg)
                self.doUpdate(arg)
        #---WIZARD---
        elif self.state == 'WIZARD':
            if ( event == 'install_wizard.state' and arg == 'DONE' ) :
                self.state = 'DONE'
                self.doUpdate(arg)
            elif event == 'print' :
                self.doPrint(arg)
                self.doUpdate(arg)
        #---AUTHORIZED---
        elif self.state == 'AUTHORIZED':
            if event == 'next' :
                self.state = 'WIZARD'
                self.doUpdate(arg)
            elif event == 'print' :
                self.doPrint(arg)
                self.doUpdate(arg)
        #---REGISTER---
        elif self.state == 'REGISTER':
            if event == 'print' :
                self.doPrint(arg)
                self.doUpdate(arg)
            elif ( event == 'id_registrator.state' and arg == 'FAILED' ) and not self.flagCmdLine :
                self.state = 'INPUT_NAME'
                self.doShowOutput(arg)
                self.doUpdate(arg)
            elif ( event == 'id_registrator.state' and arg in [ 'DONE' , 'FAILED' ] ) and self.flagCmdLine :
                self.state = 'DONE'
                self.doUpdate(arg)
            elif ( event == 'id_registrator.state' and arg == 'DONE' ) and not self.flagCmdLine :
                self.state = 'AUTHORIZED'
                self.doUpdate(arg)


    def isNameValid(self, arg):
        """
        Condition method.
        """

    def doPrint(self, arg):
        """
        Action method.
        """

    def doPrintIncorrectName(self, arg):
        """
        Action method.
        """

    def doClearOutput(self, arg):
        """
        Action method.
        """

    def doPasteKey(self, arg):
        """
        Action method.
        """

    def doShowOutput(self, arg):
        """
        Action method.
        """

    def doReadKey(self, arg):
        """
        Action method.
        """

    def doInit(self, arg):
        """
        Action method.
        """

    def doUpdate(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

