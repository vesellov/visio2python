

"""
.. module:: list_files_orator
.. role:: red

BitPie.NET list_files_orator() Automat

.. raw:: html

    <a href="list_files_orator.png" target="_blank">
    <img src="list_files_orator.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`inbox-files`
    * :red:`init`
    * :red:`local-files-done`
    * :red:`need-files`
    * :red:`timer-15sec`
"""

import automat

_ListFilesOrator = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _ListFilesOrator
    if _ListFilesOrator is None:
        # set automat name and starting state here
        _ListFilesOrator = ListFilesOrator('list_files_orator', 'LOCAL_FILES')
    if event is not None:
        _ListFilesOrator.automat(event, arg)
    return _ListFilesOrator


class ListFilesOrator(automat.Automat):
    """
    This class implements all the functionality of the ``list_files_orator()`` state machine.
    """

    timers = {
        'timer-15sec': (15.0, ['REMOTE_FILES']),
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
        #---LOCAL_FILES---
        if self.state == 'LOCAL_FILES':
            if event == 'local-files-done' and p2p_connector.A().state is 'CONNECTED' :
                self.state = 'REMOTE_FILES'
                self.doRequestRemoteFiles(arg)
            elif event == 'local-files-done' and p2p_connector.A().state is not 'CONNECTED' :
                self.state = 'NO_FILES'
        #---NO_FILES---
        elif self.state == 'NO_FILES':
            if event == 'need-files' :
                self.state = 'LOCAL_FILES'
                self.doReadLocalFiles(arg)
            elif event == 'init' :
                pass
        #---REMOTE_FILES---
        elif self.state == 'REMOTE_FILES':
            if ( event == 'timer-15sec' and self.isSomeListFilesReceived(arg) ) or ( event == 'inbox-files' and self.isAllListFilesReceived(arg) ) :
                self.state = 'SAW_FILES'
            elif event == 'timer-15sec' and not self.isSomeListFilesReceived(arg) :
                self.state = 'NO_FILES'
        #---SAW_FILES---
        elif self.state == 'SAW_FILES':
            if event == 'need-files' :
                self.state = 'LOCAL_FILES'
                self.doReadLocalFiles(arg)


    def isSomeListFilesReceived(self, arg):
        """
        Condition method.
        """

    def isAllListFilesReceived(self, arg):
        """
        Condition method.
        """

    def doRequestRemoteFiles(self, arg):
        """
        Action method.
        """

    def doReadLocalFiles(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

