from vanilla import *

class DockingSplitView(SplitView):
    '''
        This docking view has an option to reset the paneDescription
    '''
    def __init__(self, posSize, paneDescriptions, isVertical=True,
            dividerStyle="thin", dividerThickness=None, dividerColor=None,
            autosaveName=None,
            # deprecated
            dividerImage=None):
        super(SplitView, self).__init__( posSize, paneDescriptions, isVertical=isVertical,
            dividerStyle=dividerStyle, dividerThickness=dividerThickness, dividerColor=dividerColor,
            autosaveName=autosaveName,
            # deprecated
            dividerImage=dividerImage)

    def set(self, paneDescription):
        self._breakCycles()
        self._paneDescriptions = paneDescription
        self._setupPanes()


class SplitViewDemo(object):

    def __init__(self):
        self.w = Window((200, 200), "SplitView Demo", minSize=(100, 100))
        list1 = List((0, 0, -0, 100), ["A", "B", "C"])
        list2 = List((0, 0, -0, 100), ["a", "b", "c"])
        paneDescriptors = [
            dict(view=list1, identifier="pane1"),
            # dict(view=list2, identifier="pane2"),
        ]
        self.w.splitView = DockingSplitView((0, 0, -0, -0), paneDescriptors)
        paneDescriptors = [
            dict(view=list1, identifier="pane1"),
            dict(view=list2, identifier="pane2"),
        ]

        self.w.splitView.set( paneDescriptors )
        self.w.open()

if __name__ == "__main__":
    from test.testTools import executeVanillaTest

    executeVanillaTest(SplitViewDemo)