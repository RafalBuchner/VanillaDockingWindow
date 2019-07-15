from AppKit import *
from vanilla.vanillaWindows import *
from views import DockedWindowView, ContentContainerView
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
        self._content = ContentContainerView(self)
        self.dockingWindows = DockingWindowsList(self, dockingWindows)
        self.dockingWindows += dockingWindows
        self.dockedWindows = []

    @python_method
    def setChildWindows(self, dockedWindows):
        for window in dockedWindows:
            self.dockWindow(window)

    @python_method
    def _dockWindow(self, dockingWindow):
        if isinstance(dockingWindow, Window) and dockingWindow in self.dockingWindows.windowList:
            view = DockedWindowView(dockingWindow)
            viewName = 'child_%s_%s' % (len(self.dockedWindows), dockingWindow.__class__.__name__)
            setattr(self, viewName, view)
            self.dockedWindows.append(dockingWindow)
            dockingWindow.close()
            print(self.__dict__)
            dockingWindow.unbind('move')

    # EVENTS
    @python_method
    def _dockingWindowsUpdateEvent(self, dockingWindows):
        print(">>>>> ", dockingWindows)\

    @python_method
    def _dockingWindowMoveCallback(self, dockingWindow):
        print('dockingWindowMoveCallback')
        self._content.windowIsAbove(dockingWindow)

    @python_method
    def windowWillClose_(self, notification):
        super(WindowDockReciever, self).windowWillClose_(notification)




if __name__ == "__main__":
    from test.testTools import executeVanillaTest
    from vanilla import Group

    class WindowDemo(object):
        def __init__(self):
            def _ColorWin(color):
                win = Window((20, 200, 200, 270), minSize=(200, 270), title="Docked Window Demo")
                win.color = Group((0,0,-0,-0))
                win.color.getNSView().setWantsLayer_(True)
                win.color.getNSView().layer().setBackgroundColor_(color.CGColor())
                return win

            self.redW = _ColorWin(NSColor.redColor())
            self.redW.getNSWindow().setAlphaValue_(.2)
            self.redW.open()

            frame = self.redW.getNSWindow().frame()
            help(frame.size)


            self.blueW = _ColorWin(NSColor.blueColor())
            self.blueW.open()

            self.orangeW = _ColorWin(NSColor.orangeColor())
            self.orangeW.open()

            dockingWindows = [
                self.redW, self.blueW, self.orangeW
            ]

            self.w = WindowDockReciever((231, 111, 400, 370), dockingWindows=dockingWindows, minSize=(400, 370),
                                        title="Docking Window Demo")
            self.w.open()

        def cb(self, sender):
            print(sender)

    executeVanillaTest(WindowDemo)
    # WindowDemo()
