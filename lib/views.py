from vanilla import Group, TextBox, GradientButton
from vanilla.vanillaBase import VanillaBaseObject, _flipFrame
from AppKit import NSColor, NSPoint

# key = placement, value = (paneDescription index, splitView isVertical)
dockingOptions = {
    'top' : (0, True),
    'bottom' : (-1, True),
    'left' : (0, False),
    'right' : (-1, False),
    'center' : None, # special option that later would create tabbed window
}

class SimpleRect(VanillaBaseObject):
    dockingRectThickness = 20
    dockingRectPosSizes = {
        'top'    : (0,0,-0,dockingRectThickness),
        'bottom' : (0,-dockingRectThickness,-0,dockingRectThickness),
        'left'   : (0,0,dockingRectThickness,-0),
        'right'  : (-dockingRectThickness,0,dockingRectThickness,-0),
    }
    def __init__(self, posSize):
        self._nsObject = SimpleRectView.alloc().init()
        self._posSize = posSize
        self._setAutosizingFromPosSize(posSize)

class DockingGroup(Group):
    def getParentWindowPosSize(self):
        parentWindow = self.getNSView().window()
        frame = parentWindow.frame()
        l, t, w, h = _flipFrame(parentWindow.screen().visibleFrame(), frame)
        titlebarHeight = self._calculateParentWindowTitlebarHeight()
        t += titlebarHeight
        h -= titlebarHeight
        return (l, t, w, h)

    def _calculateParentWindowTitlebarHeight(self):
        parentWindow = self.getNSView().window()
        windowFrame = parentWindow.frame()
        contentHeight = parentWindow.contentRectForFrameRect_(windowFrame).size.height
        titleBarHeight = windowFrame.size.height - contentHeight
        return titleBarHeight

    def windowIsAbove(self, dockingWindow):

        winX, winY, winW, winH = dockingWindow.getPosSize()

        titleBarHeight = self._calculateParentWindowTitlebarHeight()


        x, y = (winX+winW/2, winY - titleBarHeight/2)
        gx,gy,gw,gh = self.getParentWindowPosSize()
        titleBarOnDockingGroup = NSPoint(-(gx-x),-(gy-y))
        print(titleBarOnDockingGroup    )
        ### WORK HERE!!!
        ### APPLY THE dockingRectPosSizes TO CHECK WHERE DOCKING WILL TAKE A PLACE!!!





class ContentContainerView(DockingGroup):
    '''
        content view, that docks the rest of the windows
    '''
    def __init__(self, WindowDockReciever):
        self.WindowDockReciever = WindowDockReciever
        super(ContentContainerView, self).__init__(posSize=(0, 0, -0, -0), blendingMode=None)
        self._nsObject.setWantsLayer_(True)





class DockedWindowView(Group):
    '''
        DockedWindowView
        group that represents docked windows
    '''
    titleHeight = 14

    def __init__(self, dockingWindow):
        self._dockingWindow = dockingWindow

        testPosSize = (0,0,-100,-100) ### TEST
        blendingMode = None  # ? check what exacly it does
        super(DockedWindowView, self).__init__(posSize=testPosSize, blendingMode=blendingMode)

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