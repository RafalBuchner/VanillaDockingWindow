from vanilla import *
from lib.windowDockReciever import WindowDockReciever
from lib.test.testTools import executeVanillaTest


class DemoDocking:
    def __init__(self):
        self.dockingWindow1 = Window((100, 100, 100, 100), "dockingWindow1")
        self.dockingWindow1.open()

        self.dockingWindow2 = Window((100, 300, 100, 100), "dockingWindow2")
        self.dockingWindow2.open()

        self.dockingWindow3 = Window((100, 500, 100, 100), "dockingWindow3")
        self.dockingWindow3.open()

        self.normalWindow = Window((100, 500, 100, 100), "normalWindow")
        self.normalWindow.open()

        dockingWindows = [
            self.dockingWindow1,
            self.dockingWindow2,
            self.dockingWindow3
        ]

        self.dockReciever = WindowDockReciever((250, 200, 200, 200),
                                               title="DockRecieverDemo", dockingWindows=dockingWindows, minSize=(200,200))
        self.dockReciever.open()

executeVanillaTest(DemoDocking)