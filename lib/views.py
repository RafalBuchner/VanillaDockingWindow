from vanilla import Group, TextBox, GradientButton
from vanilla.vanillaBase import VanillaBaseObject, _flipFrame
from AppKit import NSColor, NSPoint, NSEvent, NSLeftMouseUpMask
from dockingSplitView import DockingSplitView
# from copy import deepcopy

titleHeight = 14
dockingRectThickness = 55
# key = placement, value = (paneDescription index, splitView isVertical)
dockingSplitOptions = {
    'top' : (0, True),
    'bottom' : (-1, True),
    'left' : (0, False),
    'right' : (-1, False),
    'center' : None, # special option that later would create tabbed window
}

class SimpleRect(VanillaBaseObject):

    def __init__(self, posSize):
        self._nsObject = SimpleRectView.alloc().init()
        self._posSize = posSize
        self._setAutosizingFromPosSize(posSize)


class AbstractDockingGroup(Group):

    dockingRectPosSizes = {
        'top': (0, 0, -0, dockingRectThickness),
        'bottom': (0, -dockingRectThickness, -0, dockingRectThickness),
        'left': (0, 0, dockingRectThickness, -0),
        'right': (-dockingRectThickness, 0, dockingRectThickness, -0),
        # 'center'  : (dockingRectThickness*2,dockingRectThickness*2,-dockingRectThickness*2,-dockingRectThickness*2),
    }

    def __init__(self, posSize=(0, 0, -0, -0), blendingMode=None):
        super(AbstractDockingGroup, self).__init__(posSize=posSize, blendingMode=blendingMode)
        for position in self.dockingRectPosSizes:
            self.__createDockBar(position)
        self.assignedWindows = []
        self.direction = None
        self.splitCount = 0

        # #prev
        # self.getNSView().setWantsLayer_(True)
        # self.getNSView().layer().setBackgroundColor_(NSColor.greenColor().CGColor())

    def __createDockBar(self, position):
        '''
            creates dockbar, which are next to the  edges of the content view
        '''
        dockBarObj = Group(self.dockingRectPosSizes[position], blendingMode=None)
        objBarView = dockBarObj.getNSView()
        objBarView.dockBarPositionName = position
        objBarView.setWantsLayer_(True)
        objBarView.layer().setBackgroundColor_(NSColor.clearColor().CGColor())
        objName = f"{position}_dockbar"
        setattr(self, objName, dockBarObj)

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

    def mouseDragged(self):
        self.mouseDragged = True

    def windowIsAbove(self, dockingWindow):
        '''
            checks whenever dragged docking window is above any dock bar
        '''

        winX, winY, winW, winH = dockingWindow.getPosSize()

        titleBarHeight = self._calculateParentWindowTitlebarHeight()

        x, y = (winX + winW / 2, winY - titleBarHeight / 2)
        px, py, pw, ph = self.getParentWindowPosSize()
        titleBarOnDockingGrouploc = NSPoint(pw - (px - x) - pw, (py - y) + ph)
        isDockingWindowAbove = False
        dockingPosition = None
        for position in self.dockingRectPosSizes.keys():
            dockBarObj = getattr(self, f'{position}_dockbar', None)
            if dockBarObj is not None:
                view = dockBarObj.getNSView().hitTest_(titleBarOnDockingGrouploc)
                if view is not None:
                    dockBarObj.getNSView().layer().setBackgroundColor_(NSColor.orangeColor().CGColor())
                    dockingPosition = position
                    isDockingWindowAbove = True
                else:
                    dockBarObj.getNSView().layer().setBackgroundColor_(NSColor.clearColor().CGColor())
        if isDockingWindowAbove:
            dockingWindow.getNSWindow().setAlphaValue_(.4)
        else:
            dockingWindow.getNSWindow().setAlphaValue_(1)
        return dockingPosition, self

    def _clearColors(self):
        for position in self.dockingRectPosSizes.keys():
            dockBarObj = getattr(self, f'{position}_dockbar', None)
            dockBarObj.getNSView().layer().setBackgroundColor_(NSColor.clearColor().CGColor())

    def _createDockedSplit(self, direction, position, loadedWindow):
        self.direction = direction
        isVertical = True
        if direction == 'vertical': isVertical = False
        paneDescriptors = [
            dict(view=loadedWindow, identifier=f"loadedWindow_{len(self.assignedWindows)}",minSize=titleHeight,canCollapse=False),
            # dict(view=EmptyDockingGroup(), identifier="empty",minSize=0,canCollapse=False),
        ]
        if position in ("right", "bottom"):
            paneDescriptors = list(reversed(paneDescriptors))
        splitObj = DockingSplitView(
            (0,0,-0,-0), paneDescriptors, isVertical=isVertical
        )
        splitName = f"split_{self.splitCount}"
        setattr(self, splitName, splitObj)
        self._clearColors()
        self.assignedWindows += [loadedWindow]
        # self.splitCount += 1

    def _addDockedWindowToSplit(self, position, loadedWindow):
        splitName = f"split_{self.splitCount}"
        split = getattr(self, splitName, None)
        paneDescriptors = split.get()
        for pane in paneDescriptors:
            if pane['identifier']=='empty':
                paneDescriptors.remove(pane)
        newPane = dict(view=loadedWindow, identifier=f"loadedWindow_{len(self.assignedWindows)}",minSize=titleHeight,canCollapse=False)
        if position in ("top","left"):
            paneDescriptors = [newPane] + paneDescriptors
        else:
            paneDescriptors.append(newPane)
        split.set(paneDescriptors)
        self._clearColors()
        self.assignedWindows += [loadedWindow]

    def _addDockedWindowWithDifferentDirection(self, position, loadedWindow):
        isVertical = True
        if position in ('top','bottom'): isVertical = False
        oldSplitName = f"split_{self.splitCount}"
        newSplitName = f"split_{self.splitCount}"
        oldSplitObj = getattr(self, oldSplitName)
        del self.__dict__[oldSplitName]
        paneDescriptors = [
            dict(view=oldSplitObj, identifier=f"loadedWindow_{len(self.assignedWindows)}",minSize=titleHeight,canCollapse=False),
            dict(view=loadedWindow, identifier=f"loadedWindow_{len(self.assignedWindows)+1}",minSize=titleHeight,canCollapse=False),
        ]
        if position in ("top","left"):
            paneDescriptors = list(reversed(paneDescriptors))

        splitObj = DockingSplitView(
            (0,0,-0,-0), paneDescriptors, isVertical=isVertical
        )
        setattr(self, newSplitName, splitObj)
        self._clearColors()
        self.assignedWindows += [loadedWindow]


    def _dockToMe(self, position, loadedWindow):



        if position in ('top','bottom') and self.direction is None:
            self._createDockedSplit('vertical', position, loadedWindow)

        elif position in ('left', 'right') and self.direction is None:
            self._createDockedSplit('horizontal', position, loadedWindow)

        elif position in ('top','bottom') and self.direction == 'vertical':
            self._addDockedWindowToSplit(position, loadedWindow)

        elif position in ('left','right') and self.direction == 'horizontal':
            self._addDockedWindowToSplit(position, loadedWindow)

        elif position in ('top','bottom') and self.direction == 'horizontal':
            self._addDockedWindowWithDifferentDirection(position, loadedWindow)
        elif position in ('left', 'right') and self.direction == 'vertical':
            self._addDockedWindowWithDifferentDirection(position, loadedWindow)



class EmptyDockingGroup(AbstractDockingGroup):
    '''
        content view, that docks the rest of the windows
    '''

    def __init__(self, posSize=(0, 0, -0, -0), blendingMode=None):
        super(EmptyDockingGroup, self).__init__(posSize=posSize, blendingMode=blendingMode)


class LoadedDockingGroup(EmptyDockingGroup):
    '''
        DockedWindowView
        group that represents docked windows
    '''


    def __init__(self, dockingWindow):
        self._dockingWindow = dockingWindow

        testPosSize = (0, 0, -0, -0)  ### TEST
        blendingMode = None  # ? check what exacly it does
        super(LoadedDockingGroup, self).__init__(posSize=testPosSize, blendingMode=blendingMode)

        self._nsObject.setWantsLayer_(True)
        self._nsObject.layer().setBorderWidth_(1)
        self._nsObject.layer().setBorderColor_(NSColor.gridColor().CGColor())
        self.__addTitleView()
        self.__addContentView()
        self.__transferDockedContent()

    def __addTitleView(self):
        self._titleView = Group((0, 0, -0, titleHeight))
        self._dockingWindow.getTitle()
        self._titleView.title = TextBox((0, 0, -0, titleHeight), self._dockingWindow.getTitle(),
                                        sizeStyle='mini',
                                        alignment='center')
        self._titleView.undockBtn = GradientButton((-titleHeight, 0, titleHeight, titleHeight),
                                                   title="❏", bordered=False, callback=self._undock, sizeStyle='mini')
        self._titleView.getNSView().setWantsLayer_(True)
        self._titleView.getNSView().layer().setBackgroundColor_(NSColor.gridColor().CGColor())

    def __addContentView(self):
        self._contentView = Group((0, titleHeight, -0, -0))

    def __transferDockedContent(self):
        for objName in self._dockingWindow.__dict__:
            obj = getattr(self._dockingWindow, objName)
            if isinstance(obj, VanillaBaseObject):
                setattr(self._contentView, objName, obj)
                # I don't know if it is a proper way to change the posi

    def _undock(self, sender):
        print("undock not implemented yet")
