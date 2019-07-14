from AppKit import *
from vanilla.vanillaWindows import *
from vanilla.vanillaBase import VanillaBaseObject
from vanilla import Group, GradientButton, TextBox



class DockedView(Group):
    titleHeight = 14

    def __init__(self, dockingWindow):
        self._dockingWindow = dockingWindow

        testPosSize = (0,0,-100,-100) ### TEST
        blendingMode = None  # ? check what exacly it does
        super(DockedView, self).__init__(posSize=testPosSize, blendingMode=blendingMode)

        self._nsObject.setWantsLayer_(True)
        self._nsObject.layer().setBorderWidth_(1)
        self._nsObject.layer().setBorderColor_(NSColor.gridColor().CGColor())
        self.__addTitleView()
        self.__addContentView()
        self.__transferDockedContent()

    def __addTitleView(self):
        self._titleView = Group((0, 0, -0, self.titleHeight))
        self._dockingWindow.getTitle()
        self._titleView.title = TextBox((0, 0, -0, self.titleHeight), self._dockingWindow.getTitle(),
                                         sizeStyle='mini',
                                         alignment='center')
        self._titleView.undockBtn = GradientButton((-self.titleHeight, 0, self.titleHeight, self.titleHeight),
                                                    title="❏", bordered=False, callback=self._undock,sizeStyle='mini')
        self._titleView.getNSView().setWantsLayer_(True)
        self._titleView.getNSView().layer().setBackgroundColor_(NSColor.gridColor().CGColor())

    def __addContentView(self):
        self._contentView = Group((0,self.titleHeight,-0,-0))

    def __transferDockedContent(self):
        for objName in self._dockingWindow.__dict__:
            obj = getattr(self._dockingWindow, objName)
            if isinstance(obj, VanillaBaseObject):
                setattr(self._contentView, objName, obj)
                # I don't know if it is a proper way to change the posi

    def _undock(self, sender):
        print("undock not implemented yet")

class DockingWindowsList(object):
    def __init__(self, dockWindow, windowList):
        self.windowList = windowList
        self.dockWindow = dockWindow
        self.__callEvent()

    def __callEvent(self):
        self.dockWindow._dockingWindowsUpdateEvent(self)

    def append(self, object):
        self.__callEvent()
        self.windowList.append(object)

    def __add__(self, value):
        self.__callEvent()
        self.windowList.__add__(value)

    def __iadd__(self, value):
        self.__callEvent()
        self.windowList += value
        return self

    def __len__(self):
        return len(self.windowList)

    def remove(self, object):
        self.__callEvent()
        self.windowList.remove(object)


class WindowDockReciever(Window):
    '''
        - you need to declare what window objects are dockable (dockingWIndow parametr
        - 'dockedWindows' attribute says which window right now is being docked

    '''
    nsWindowStyleMask = NSTitledWindowMask | NSUnifiedTitleAndToolbarWindowMask

    # nsWindowStyleMask = NSWindowStyleMaskFullSizeContentView | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable
    def __init__(self, posSize, title="", dockingWindows=[], minSize=None, maxSize=None, textured=False,
                 autosaveName=None, closable=True, miniaturizable=True, initiallyVisible=True,
                 fullScreenMode=None, titleVisible=True, fullSizeContentView=False, screen=None):
        super(WindowDockReciever, self).__init__(posSize, title, minSize, maxSize, textured, autosaveName, closable,
                                                 miniaturizable, initiallyVisible, fullScreenMode, titleVisible,
                                                 fullSizeContentView, screen)
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
            view = DockedView(dockingWindow)
            viewName = 'child_%s_%s' % (len(self.dockedWindows), dockingWindow.__class__.__name__)
            setattr(self, viewName, view)
            self.dockedWindows.append(dockingWindow)
            dockingWindow.close()
            print(self.__dict__)

    @python_method
    def _dockingWindowsUpdateEvent(self, dockingWindows):
        print(">>>>> ", dockingWindows)

    @python_method
    def windowWillClose_(self, notification):
        super(WindowDockReciever, self).windowWillClose_(notification)

class WindowDemo(object):
    def __init__(self):
        # self.w.btn = GradientButton((0,0,100,100),title="OK",callback=self.cb)
        self.w2 = Window((20, 200, 200, 270), minSize=(200, 270), title="Docked Window Demo")
        self.w2.open()
        self.w2.btn = GradientButton((0, 0, 100, 100), title="OK", callback=self.cb)

        self.w = WindowDockReciever((231, 111, 400, 370), dockingWindows=[self.w2], minSize=(400, 370),
                                    title="Docking Window Demo")
        self.w._dockWindow(self.w2)
        self.w.open()

    def cb(self, sender):
        print(sender)


if __name__ == "__main__":
    from test.testTools import executeVanillaTest

    executeVanillaTest(WindowDemo)
    # WindowDemo()
