from AppKit import *
from vanilla.vanillaWindows import *
from views import LoadedDockingGroup, EmptyDockingGroup
from helperObjects import *
from dockingSplitView import DockingSplitView


class WindowDockReciever(Window):
    '''
        - you need to declare what window objects are dockable (dockingWIndow parametr
        - 'dockedWindows' attribute says which window right now is being docked

    '''
    nsWindowStyleMask = NSTitledWindowMask | NSUnifiedTitleAndToolbarWindowMask

    def __init__(self, posSize, title="", dockingWindows=[], minSize=None, maxSize=None, textured=False,
                 autosaveName=None, closable=True, miniaturizable=True, initiallyVisible=True,
                 fullScreenMode=None, titleVisible=True, fullSizeContentView=False, screen=None):
        super(WindowDockReciever, self).__init__(posSize, title, minSize, maxSize, textured, autosaveName, closable,
                                                 miniaturizable, initiallyVisible, fullScreenMode, titleVisible,
                                                 fullSizeContentView, screen)
        self._content = EmptyDockingGroup()
        self.dockingWindows = DockingWindowsList(self, dockingWindows)
        self.dockingWindows += dockingWindows
        self.dockedWindows = []

        NSEvent.addLocalMonitorForEventsMatchingMask_handler_(NSLeftMouseUpMask, self.mouseUp)

    @python_method
    def mouseUp(self, event):
        print(self.currentlyDockingWinodow_Position)
        self._dockWindow()

        self.currentlyDockingWinodow_Position = (None, None, None)

    @python_method
    def setChildWindows(self, dockedWindows):
        for window in dockedWindows:
            self.dockWindow(window)

    @python_method
    def _dockWindow(self):
        dockingWindow, position, dockGroup = self.currentlyDockingWinodow_Position

        self._dockWindowTEST(dockingWindow, position, dockGroup)

    @python_method
    def _dockWindowTEST(self,dockingWindow, position, dockGroup):
        if position is None:
            return
        if isinstance(dockingWindow,Window) \
                and dockingWindow in self.dockingWindows.windowList \
                and dockingWindow not in self.dockedWindows:
            loadedWindow = LoadedDockingGroup(dockingWindow)
            viewName = 'child_%s_%s' % (len(self.dockedWindows), dockingWindow.__class__.__name__)
            # setattr(self, viewName, loadedWindow)
            self.dockedWindows.append(dockingWindow)
            dockingWindow.close()
            dockGroup._dockToMe(position, loadedWindow)
            setattr(self, viewName, dockGroup)
            if hasattr(dockingWindow, '_bindings'):
                dockingWindow.unbind('move', self._dockingWindowMoveCallback)

    # EVENTS
    @python_method
    def _dockingWindowsUpdateEvent(self, dockingWindows):
        # print(">>>>> ", dockingWindows)
        pass

    @python_method
    def _dockingWindowMoveCallback(self, dockingWindow):
        dockingPosition, dockGroup = self._content.windowIsAbove(dockingWindow)
        self.currentlyDockingWinodow_Position = (dockingWindow, dockingPosition, dockGroup)

    @python_method
    def windowWillClose_(self, notification):
        super(WindowDockReciever, self).windowWillClose_(notification)


testNum = 0

if __name__ == "__main__":
    from test.testTools import executeVanillaTest
    from vanilla import Group, GradientButton, TextBox

    class WindowDemo(object):
        def __init__(self):

            def _testWind():
                win = Window((20, 200, 200, 270), minSize=(200, 270), title="Docked Window Demo")
                win.color = Group((0, 0, -0, -0))
                win.color.txt = TextBox((0,0,-0,-0),f"demo window {globals()['testNum']}",alignment='center')
                globals()['testNum'] = globals()['testNum'] + 1
                # win.color.getNSView().setWantsLayer_(True)
                # win.color.getNSView().layer().setBackgroundColor_(color.CGColor())
                # win.btn = GradientButton((10, 10, 50, 50),
                #                          title="❏", sizeStyle='regular')
                return win

            # self.redW = _ColorWin(NSColor.redColor())
            # self.redW.open()
            #
            # self.blueW = _ColorWin(NSColor.blueColor())
            # self.blueW.open()

            self.w1 = _testWind()
            self.w1.open()
            self.w2 = _testWind()
            self.w2.open()
            self.w3 = _testWind()
            self.w3.open()
            self.w4 = _testWind()
            self.w4.open()
            self.w5 = _testWind()
            self.w5.open()
            self.w6 = _testWind()
            self.w6.open()

            dockingWindows = [
                self.w1,
                self.w2,
                self.w3,
                self.w4,
                self.w5,
                self.w6,
            ]

            self.w = WindowDockReciever((231, 111, 400, 370), dockingWindows=dockingWindows, minSize=(400, 370),
                                        title="Docking Window Demo")
            self.w._dockWindowTEST(self.w1, 'left', self.w._content)
            self.w._dockWindowTEST(self.w2, 'left', self.w._content)
            self.w._dockWindowTEST(self.w3, 'bottom', self.w._content)
            self.w._dockWindowTEST(self.w4, 'left', self.w._content)
            # self.w._dockWindowTEST(self.w5, 'left', self.w._content) # ERRPR NECAISE OF DIRECTION OF THE CONTENT VIEW
            self.w.open()

        def cb(self, sender):
            print(sender)


    executeVanillaTest(WindowDemo)
    # WindowDemo()
