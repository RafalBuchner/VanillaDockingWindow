from vanilla import Group, TextBox, GradientButton
from vanilla.vanillaBase import VanillaBaseObject
from AppKit import NSColor

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