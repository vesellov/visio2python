

"""
.. module:: id_server
.. role:: red

BitPie.NET id_server() Automat

.. raw:: html

    <a href="id_server.png" target="_blank">
    <img src="id_server.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`incoming-identity-file`
    * :red:`server-down`
    * :red:`shutdown`
    * :red:`start`
    * :red:`stop`
"""

import automat

_IdServer = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _IdServer
    if _IdServer is None:
        # set automat name and starting state here
        _IdServer = IdServer('id_server', 'AT_STARTUP')
    if event is not None:
        _IdServer.automat(event, arg)
    return _IdServer


class IdServer(automat.Automat):
    """
    This class implements all the functionality of the ``id_server()`` state machine.
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
            if event == 'start' :
                self.state = 'LISTEN'
                self.doSaveParams(arg)
                self.doSetUp(arg)
        #---LISTEN---
        elif self.state == 'LISTEN':
            if event == 'shutdown' :
                self.state = 'CLOSED'
                self.doSetDown(arg)
                self.doDestroyMe(arg)
            elif event == 'incoming-identity-file' :
                self.doCheckAndSaveIdentity(arg)
            elif event == 'stop' :
                self.state = 'DOWN'
                self.Restart=False
                self.doSetDown(arg)
        #---STOPPED---
        elif self.state == 'STOPPED':
            if event == 'shutdown' :
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'start' :
                self.state = 'LISTEN'
                self.doSaveParams(arg)
                self.doSetUp(arg)
        #---CLOSED---
        elif self.state == 'CLOSED':
            pass
        #---DOWN---
        elif self.state == 'DOWN':
            if event == 'server-down' and not self.Restart :
                self.state = 'STOPPED'
            elif event == 'server-down' and self.Restart :
                self.state = 'LISTEN'
                self.doSetUp(arg)
            elif event == 'start' :
                self.doSaveParams(arg)
                self.Restart=True


    def doSetUp(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _IdServer
        del _IdServer
        _IdServer = None

    def doSaveParams(self, arg):
        """
        Action method.
        """

    def doCheckAndSaveIdentity(self, arg):
        """
        Action method.
        """

    def doSetDown(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

