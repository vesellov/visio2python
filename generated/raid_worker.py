

"""
.. module:: raid_worker
.. role:: red

BitPie.NET raid_worker Automat

.. raw:: html

    <a href="raid_worker.png" target="_blank">
    <img src="raid_worker.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`init`
    * :red:`new-task`
    * :red:`process-started`
    * :red:`shutdown`
    * :red:`task-done`
    * :red:`task-started`
    * :red:`timer-1min`
"""

import automat

_RaidWorker = None

def A(event=None, arg=None):
    """
    Access method to interact with the state machine.
    """
    global _RaidWorker
    if _RaidWorker is None:
        # set automat name and starting state here
        _RaidWorker = RaidWorker('raid_worker', 'WORK')
    if event is not None:
        _RaidWorker.automat(event, arg)
    return _RaidWorker


class RaidWorker(automat.Automat):
    """
    This class implements all the functionality of the ``raid_worker()`` state machine.
    """

    timers = {
        'timer-1min': (60, ['READY']),
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
        #---WORK---
        if self.state == 'WORK':
            if event == 'task-done' and not self.isSomeActive(arg) and not self.isMoreTasks(arg) :
                self.state = 'READY'
                self.doReportTaskDone(arg)
            elif event == 'new-task' :
                self.doAddTask(arg)
                self.doStartTask(arg)
            elif event == 'shutdown' :
                self.state = 'CLOSED'
                self.doReportTasksFailed(arg)
                self.doKillProcess(arg)
                self.doDestroyMe(arg)
            elif event == 'task-done' and self.isMoreTasks(arg) :
                self.doReportTaskDone(arg)
                self.doStartTask(arg)
            elif event == 'task-done' and self.isSomeActive(arg) and not self.isMoreTasks(arg) :
                self.doReportTaskDone(arg)
            elif event == 'task-started' and self.isMoreTasks(arg) :
                self.doStartTask(arg)
        #---AT_STARTUP---
        elif self.state == 'AT_STARTUP':
            if event == 'init' :
                self.state = 'OFF'
                self.doInit(arg)
        #---OFF---
        elif self.state == 'OFF':
            if event == 'shutdown' :
                self.state = 'CLOSED'
                self.doKillProcess(arg)
                self.doDestroyMe(arg)
            elif event == 'process-started' and self.isSomeTasks(arg) :
                self.state = 'WORK'
                self.doStartTask(arg)
            elif event == 'new-task' :
                self.doAddTask(arg)
                self.doStartProcess(arg)
            elif event == 'process-started' and not self.isSomeTasks(arg) :
                self.state = 'READY'
        #---READY---
        elif self.state == 'READY':
            if event == 'new-task' :
                self.state = 'WORK'
                self.doAddTask(arg)
                self.doStartTask(arg)
            elif event == 'shutdown' :
                self.state = 'CLOSED'
                self.doKillProcess(arg)
                self.doDestroyMe(arg)
            elif event == 'timer-1min' :
                self.state = 'OFF'
                self.doKillProcess(arg)
        #---CLOSED---
        elif self.state == 'CLOSED':
            pass


    def isMoreTasks(self, arg):
        """
        Condition method.
        """

    def isSomeActive(self, arg):
        """
        Condition method.
        """

    def isSomeTasks(self, arg):
        """
        Condition method.
        """

    def doStartTask(self, arg):
        """
        Action method.
        """

    def doStartProcess(self, arg):
        """
        Action method.
        """

    def doReportTaskDone(self, arg):
        """
        Action method.
        """

    def doReportTasksFailed(self, arg):
        """
        Action method.
        """

    def doDestroyMe(self, arg):
        """
        Remove all references to the state machine object to destroy it.
        """
        automat.objects().pop(self.index)
        global _RaidWorker
        del _RaidWorker
        _RaidWorker = None

    def doKillProcess(self, arg):
        """
        Action method.
        """

    def doInit(self, arg):
        """
        Action method.
        """

    def doAddTask(self, arg):
        """
        Action method.
        """



def main():
    from twisted.internet import reactor
    reactor.callWhenRunning(A, 'init')
    reactor.run()

if __name__ == "__main__":
    main()

