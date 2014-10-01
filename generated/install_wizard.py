

"""
.. module:: install_wizard
.. role:: red

BitPie.NET install_wizard() Automat

.. raw:: html

    <a href="install_wizard.png" target="_blank">
    <img src="install_wizard.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`back`
    * :red:`next`
    * :red:`select-beta-test`
    * :red:`select-donator`
    * :red:`select-free-backups`
    * :red:`select-secure`
    * :red:`select-try-it`
"""

import automat

_InstallWizard = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _InstallWizard
    if _InstallWizard is None:
        # set automat name and starting state here
        _InstallWizard = InstallWizard('install_wizard', 'LAST_PAGE')
    if event is not None:
        _InstallWizard.automat(event, arg)
    return _InstallWizard


class InstallWizard(automat.Automat):
    """
    This class implements all the functionality of the ``install_wizard()`` state machine.
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
        #---LAST_PAGE---
        if self.state == 'LAST_PAGE':
            if event == 'back' :
                self.state = 'CONTACTS'
            elif event == 'next' :
                self.state = 'DONE'
        #---CONTACTS---
        elif self.state == 'CONTACTS':
            if event == 'back' :
                self.state = 'STORAGE'
            elif event == 'next' :
                self.state = 'LAST_PAGE'
                self.doSaveContacts(arg)
        #---STORAGE---
        elif self.state == 'STORAGE':
            if event == 'back' and self.isRoleSecure(arg) :
                self.state = 'MOST_SECURE'
            elif event == 'back' and self.isRoleDonator(arg) :
                self.state = 'DONATOR'
            elif event == 'back' and self.isRoleFreeBackups(arg) :
                self.state = 'FREE_BACKUPS'
            elif event == 'next' :
                self.state = 'CONTACTS'
                self.doSaveStorage(arg)
            elif event == 'back' and self.isRoleBetaTest(arg) :
                self.state = 'BETA_TEST'
        #---READY---
        elif self.state == 'READY':
            if event == 'select-secure' :
                self.state = 'MOST_SECURE'
                self.doSaveRole(arg)
            elif event == 'select-donator' :
                self.state = 'DONATOR'
                self.doSaveRole(arg)
            elif event == 'select-free-backups' :
                self.state = 'FREE_BACKUPS'
                self.doSaveRole(arg)
            elif event == 'select-try-it' :
                self.state = 'JUST_TRY_IT'
                self.doSaveRole(arg)
            elif event == 'select-beta-test' :
                self.state = 'BETA_TEST'
                self.doSaveRole(arg)
        #---JUST_TRY_IT---
        elif self.state == 'JUST_TRY_IT':
            if event == 'back' :
                self.state = 'READY'
            elif event == 'next' :
                self.state = 'LAST_PAGE'
        #---FREE_BACKUPS---
        elif self.state == 'FREE_BACKUPS':
            if event == 'back' :
                self.state = 'READY'
            elif event == 'next' :
                self.state = 'STORAGE'
                self.doSaveParams(arg)
        #---BETA_TEST---
        elif self.state == 'BETA_TEST':
            if event == 'back' :
                self.state = 'READY'
            elif event == 'next' :
                self.state = 'STORAGE'
                self.doSaveParams(arg)
        #---DONATOR---
        elif self.state == 'DONATOR':
            if event == 'back' :
                self.state = 'READY'
            elif event == 'next' :
                self.state = 'STORAGE'
        #---MOST_SECURE---
        elif self.state == 'MOST_SECURE':
            if event == 'back' :
                self.state = 'READY'
            elif event == 'next' :
                self.state = 'STORAGE'
                self.doSaveParams(arg)
        #---DONE---
        elif self.state == 'DONE':
            if event == 'back' :
                self.state = 'LAST_PAGE'


    def isRoleSecure(self, arg):
        """
        Condition method.
        """

    def isRoleFreeBackups(self, arg):
        """
        Condition method.
        """

    def isRoleBetaTest(self, arg):
        """
        Condition method.
        """

    def isRoleDonator(self, arg):
        """
        Condition method.
        """

    def doSaveRole(self, arg):
        """
        Action method.
        """

    def doSaveContacts(self, arg):
        """
        Action method.
        """

    def doSaveParams(self, arg):
        """
        Action method.
        """

    def doSaveStorage(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

