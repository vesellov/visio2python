

"""
.. module:: p2p_connector
.. role:: red

BitPie.NET p2p_connector() Automat

.. raw:: html

    <a href="p2p_connector.png" target="_blank">
    <img src="p2p_connector.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`inbox-packet`
    * :red:`init`
    * :red:`my-id-propagated`
    * :red:`my-id-updated`
    * :red:`network_connector.state`
    * :red:`ping-contact`
    * :red:`reconnect`
    * :red:`timer-20sec`
"""

import automat

_P2pConnector = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _P2pConnector
    if _P2pConnector is None:
        # set automat name and starting state here
        _P2pConnector = P2pConnector('p2p_connector', 'MY_IDENTITY')
    if event is not None:
        _P2pConnector.automat(event, arg)
    return _P2pConnector


class P2pConnector(automat.Automat):
    """
    This class implements all the functionality of the ``p2p_connector()`` state machine.
    """

    timers = {
        'timer-20sec': (20.0, ['INCOMMING?']),
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
        #---MY_IDENTITY---
        if self.state == 'MY_IDENTITY':
            if event == 'my-id-updated' and self.isMyIdentityChanged(arg) :
                self.state = 'NETWORK?'
                network_connector.A('reconnect')
            elif event == 'my-id-updated' and not self.isMyIdentityChanged(arg) :
                self.state = 'CONTACTS'
                self.doPropagateMyIdentity(arg)
        #---NETWORK?---
        elif self.state == 'NETWORK?':
            if ( event == 'network_connector.state' and arg == 'DISCONNECTED' ) :
                self.state = 'DISCONNECTED'
            elif ( event == 'network_connector.state' and arg == 'CONNECTED' ) :
                self.state = 'MY_IDENTITY'
                self.doUpdateMyIdentity(arg)
        #---DISCONNECTED---
        elif self.state == 'DISCONNECTED':
            if event == 'inbox-packet' or event == 'reconnect' or ( ( event == 'network_connector.state' and arg == 'CONNECTED' ) ) :
                self.state = 'MY_IDENTITY'
                self.doUpdateMyIdentity(arg)
            elif ( event == 'network_connector.state' and arg not in [ 'CONNECTED', 'DISCONNECTED', ] ) :
                self.state = 'NETWORK?'
            elif event == 'ping-contact' :
                self.doSendMyIdentity(arg)
        #---CONNECTED---
        elif self.state == 'CONNECTED':
            if ( event == 'network_connector.state' and arg == 'DISCONNECTED' ) :
                self.state = 'DISCONNECTED'
            elif event == 'ping-contact' :
                self.doSendMyIdentity(arg)
            elif event == 'reconnect' or ( event == 'network_connector.state' and arg == 'CONNECTED' ) :
                self.state = 'MY_IDENTITY'
                self.doUpdateMyIdentity(arg)
            elif ( event == 'network_connector.state' and arg not in [ 'CONNECTED' , 'DISCONNECTED' ] ) :
                self.state = 'NETWORK?'
        #---CONTACTS---
        elif self.state == 'CONTACTS':
            if ( ( event == 'network_connector.state' and arg == 'CONNECTED' ) ) or event == 'reconnect' :
                self.state = 'MY_IDENTITY'
                self.doUpdateMyIdentity(arg)
            elif event == 'my-id-propagated' :
                self.state = 'INCOMMING?'
                fire_hire.A('restart')
        #---INCOMMING?---
        elif self.state == 'INCOMMING?':
            if event == 'reconnect' or ( event == 'network_connector.state' and arg == 'CONNECTED' ) :
                self.state = 'MY_IDENTITY'
                self.doUpdateMyIdentity(arg)
            elif event == 'inbox-packet' and self.isUsingBestProto(arg) :
                self.state = 'CONNECTED'
                self.doInitRatings(arg)
                backup_monitor.A('restart')
                customers_rejector.A('restart')
            elif event == 'timer-20sec' or ( event == 'network_connector.state' and arg == 'DISCONNECTED' ) :
                self.state = 'DISCONNECTED'
                self.doInitRatings(arg)
            elif event == 'inbox-packet' and not self.isUsingBestProto(arg) :
                self.state = 'MY_IDENTITY'
                self.doUpdateMyIdentity(arg)
                self.doPopBestProto(arg)
        #---AT_STARTUP---
        elif self.state == 'AT_STARTUP':
            if event == 'init' :
                self.state = 'NETWORK?'
                self.doInit(arg)
                network_connector.A('init')
                backup_monitor.A('init')
                backup_db_keeper.A('init')
                list_files_orator.A('init')
                fire_hire.A('init')
                data_sender.A('init')
                raid_worker.A('init')


    def isMyIdentityChanged(self, arg):
        """
        Condition method.
        """

    def isUsingBestProto(self, arg):
        """
        Condition method.
        """

    def doSendMyIdentity(self, arg):
        """
        Action method.
        """

    def doInitRatings(self, arg):
        """
        Action method.
        """

    def doPropagateMyIdentity(self, arg):
        """
        Action method.
        """

    def doPopBestProto(self, arg):
        """
        Action method.
        """

    def doUpdateMyIdentity(self, arg):
        """
        Action method.
        """

    def doInit(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

