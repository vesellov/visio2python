

"""
.. module:: id_registrator
.. role:: red

BitPie.NET id_registrator() Automat

.. raw:: html

    <a href="id_registrator.png" target="_blank">
    <img src="id_registrator.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`id-exist`
    * :red:`id-not-exist`
    * :red:`id-server-failed`
    * :red:`id-server-response`
    * :red:`local-ip-detected`
    * :red:`my-id-exist`
    * :red:`my-id-failed`
    * :red:`my-id-sent`
    * :red:`start`
    * :red:`stun-failed`
    * :red:`stun-success`
    * :red:`timer-10sec`
    * :red:`timer-30sec`
    * :red:`timer-5sec`
"""

import automat

_IdRegistrator = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _IdRegistrator
    if _IdRegistrator is None:
        # set automat name and starting state here
        _IdRegistrator = IdRegistrator('id_registrator', 'AT_STARTUP')
    if event is not None:
        _IdRegistrator.automat(event, arg)
    return _IdRegistrator


class IdRegistrator(automat.Automat):
    """
    This class implements all the functionality of the ``id_registrator()`` state machine.
    """

    timers = {
        'timer-30sec': (30.0, ['NAME_FREE?']),
        'timer-10sec': (10.0, ['SEND_ID','REQUEST_ID']),
        'timer-5sec': (5.0, ['REQUEST_ID']),
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
        #---AT_STARTUP---
        if self.state == 'AT_STARTUP':
            if event == 'start' :
                self.state = 'ID_SERVERS?'
                self.doSaveMyName(arg)
                self.doSelectRandomServers(arg)
                self.doPingServers(arg)
                self.doPrint(self.msg('MSG_0', arg))
        #---DONE---
        elif self.state == 'DONE':
            pass
        #---FAILED---
        elif self.state == 'FAILED':
            pass
        #---ID_SERVERS?---
        elif self.state == 'ID_SERVERS?':
            if ( event == 'id-server-response' or event == 'id-server-failed' ) and self.isAllTested(arg) and self.isSomeAlive(arg) :
                self.state = 'NAME_FREE?'
                self.doRequestServers(arg)
                self.doPrint(self.msg('MSG_1', arg))
            elif ( event == 'id-server-response' or event == 'id-server-failed' ) and self.isAllTested(arg) and not self.isSomeAlive(arg) :
                self.state = 'FAILED'
                self.doPrint(self.msg('MSG_7', arg))
                self.doDestroyMe(arg)
        #---NAME_FREE?---
        elif self.state == 'NAME_FREE?':
            if event == 'id-not-exist' and self.isAllResponded(arg) and self.isFreeIDURLs(arg) :
                self.state = 'LOCAL_IP'
                self.doDetectLocalIP(arg)
                self.doPrint(self.msg('MSG_2', arg))
            elif event == 'timer-30sec' or ( event == 'id-exist' and self.isAllResponded(arg) and not self.isFreeIDURLs(arg) ) :
                self.state = 'FAILED'
                self.doPrint(self.msg('MSG_8', arg))
                self.doDestroyMe(arg)
        #---LOCAL_IP---
        elif self.state == 'LOCAL_IP':
            if event == 'local-ip-detected' :
                self.state = 'EXTERNAL_IP'
                self.doStunExternalIP(arg)
                self.doPrint(self.msg('MSG_3', arg))
        #---EXTERNAL_IP---
        elif self.state == 'EXTERNAL_IP':
            if event == 'stun-success' :
                self.state = 'SEND_ID'
                self.doCreateMyIdentity(arg)
                self.doSendMyIdentity(arg)
                self.doPrint(self.msg('MSG_4', arg))
            elif event == 'stun-failed' :
                self.state = 'FAILED'
                self.doPrint(self.msg('MSG_9', arg))
                self.doDestroyMe(arg)
        #---SEND_ID---
        elif self.state == 'SEND_ID':
            if event == 'my-id-sent' :
                self.state = 'REQUEST_ID'
                self.doRequestMyIdentity(arg)
                self.doPrint(self.msg('MSG_5', arg))
            elif event == 'my-id-failed' :
                self.state = 'FAILED'
                self.doPrint(self.msg('MSG_10', arg))
                self.doDestroyMe(arg)
            elif event == 'timer-10sec' :
                self.state = 'FAILED'
                self.doPrint(self.msg('MSG_13', arg))
                self.doDestroyMe(arg)
        #---REQUEST_ID---
        elif self.state == 'REQUEST_ID':
            if event == 'my-id-exist' and self.isMyIdentityValid(arg) :
                self.state = 'DONE'
                self.doSaveMyIdentity(arg)
                self.doDestroyMe(arg)
                self.doPrint(self.msg('MSG_6', arg))
            elif event == 'timer-5sec' :
                self.doRequestMyIdentity(arg)
            elif event == 'timer-10sec' :
                self.state = 'FAILED'
                self.doPrint(self.msg('MSG_12', arg))
                self.doDestroyMe(arg)
            elif event == 'my-id-exist' and not self.isMyIdentityValid(arg) :
                self.state = 'FAILED'
                self.doPrint(self.msg('MSG_11', arg))
                self.doDestroyMe(arg)


    def isMyIdentityValid(self, arg):
        """
        Condition method.
        """

    def isSomeAlive(self, arg):
        """
        Condition method.
        """

    def isAllTested(self, arg):
        """
        Condition method.
        """

    def isAllResponded(self, arg):
        """
        Condition method.
        """

    def isFreeIDURLs(self, arg):
        """
        Condition method.
        """

    def doSelectRandomServers(self, arg):
        """
        Action method.
        """

    def doCreateMyIdentity(self, arg):
        """
        Action method.
        """

    def doSendMyIdentity(self, arg):
        """
        Action method.
        """

    def doPrint(self, arg):
        """
        Action method.
        """

    def doRequestServers(self, arg):
        """
        Action method.
        """

    def doSaveMyName(self, arg):
        """
        Action method.
        """

    def doPingServers(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _IdRegistrator
        del _IdRegistrator
        _IdRegistrator = None

    def doDetectLocalIP(self, arg):
        """
        Action method.
        """

    def doStunExternalIP(self, arg):
        """
        Action method.
        """

    def doRequestMyIdentity(self, arg):
        """
        Action method.
        """

    def doSaveMyIdentity(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

