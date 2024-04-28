import sys
import time

from PySide6.QtCore import QThread, QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QWidgetAction, QFileDialog


class Receiver(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.runner = None

    # The bool in the type for the slot should be whatever you want your function to have as input
    @Slot(bool)
    def receive(self, isActive):
        print('Active?', isActive)

    def startLoop(self):
        # threadCount = QThreadPool.globalInstance().maxThreadCount()
        pool = QThreadPool.globalInstance()

        # None should be the item you want to loop through, if it is not a group it should still work
        self.runner = Sender(None)
        # pool.start starts the loop
        pool.start(self.runner)


class Sender(QRunnable, QObject):
    # Again bool should be whatever you want yourfunction to be
    sendThing = Signal(bool)

    def __init__(self, loop):
        # a call to super().__init__() should work, but just use this
        QRunnable.__init__(self)
        QObject.__init__(self)

        # Instance Variables
        self.loop = loop
        self.running = True

    def run(self):
        while self.running:
            for i in self.loop:
                # Add any if's to check the status of things here
                # This is what sends the signal
                self.sendThing.emit(i)
                time.sleep(.05)

    def stop(self):
        self.running = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Receiver()
    widget.show()
    # Start the loop BEFORE connecting your signal
    widget.startLoop()
    #################

    # There will be no typehints for this, but this is how it is formatted
    widget.runner.sendThing.connect(widget.receive)

    # Sends code so the loop stops
    if app.exit():
        widget.runner.stop()
    sys.exit(app.exec())
