

"""
.. module:: contact_status
.. role:: red

BitPie.NET contact_status() Automat

.. raw:: html

    <a href="contact_status.png" target="_blank">
    <img src="contact_status.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`file-sent`
    * :red:`inbox-packet`
    * :red:`outbox-packet`
    * :red:`sent-done`
    * :red:`sent-failed`
    * :red:`timer-20sec`
"""

import automat

_ContactStatus = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _ContactStatus
    if _ContactStatus is None:
        # set automat name and starting state here
        _ContactStatus = ContactStatus('contact_status', 'OFFLINE')
    if event is not None:
        _ContactStatus.automat(event, arg)
    return _ContactStatus


class ContactStatus(automat.Automat):
    """
    This class implements all the functionality of the ``contact_status()`` state machine.
    """

    timers = {
        'timer-20sec': (20.0, ['PING','ACK?']),
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
        #---OFFLINE---
        if self.state == 'OFFLINE':
            if event == 'inbox-packet' :
                self.state = 'CONNECTED'
                self.doRememberTime(arg)
                self.doRepaint(arg)
            elif event == 'outbox-packet' and self.isPingPacket(arg) :
                self.state = 'PING'
                self.AckCounter=0
                self.doRepaint(arg)
        #---CONNECTED---
        elif self.state == 'CONNECTED':
            if event == 'sent-failed' and self.isDataPacket(arg) :
                self.state = 'OFFLINE'
                self.doRepaint(arg)
            elif event == 'outbox-packet' and self.isPingPacket(arg) :
                self.state = 'PING'
                self.AckCounter=0
                self.doRepaint(arg)
        #---PING---
        elif self.state == 'PING':
            if event == 'timer-20sec' or ( event == 'sent-failed' and self.AckCounter==1 ) :
                self.state = 'OFFLINE'
                self.doRepaint(arg)
            elif event == 'sent-done' :
                self.state = 'ACK?'
                self.AckCounter=0
            elif event == 'file-sent' :
                self.AckCounter+=1
            elif event == 'inbox-packet' :
                self.state = 'CONNECTED'
                self.doRememberTime(arg)
                self.doRepaint(arg)
            elif event == 'sent-failed' and self.AckCounter>1 :
                self.AckCounter-=1
        #---ACK?---
        elif self.state == 'ACK?':
            if event == 'inbox-packet' :
                self.state = 'CONNECTED'
                self.doRememberTime(arg)
                self.doRepaint(arg)
            elif event == 'timer-20sec' :
                self.state = 'OFFLINE'
            elif event == 'outbox-packet' and self.isPingPacket(arg) :
                self.state = 'PING'
                self.AckCounter=0
                self.doRepaint(arg)


    def isDataPacket(self, arg):
        """
        Condition method.
        """

    def isPingPacket(self, arg):
        """
        Condition method.
        """

    def doRememberTime(self, arg):
        """
        Action method.
        """

    def doRepaint(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

