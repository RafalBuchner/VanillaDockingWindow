
class DockingWindowsList(object):
    '''
        List that contains windows, that are included into docking
        It is only used inside of the WindowDockReciever class.
        Its main purpose is to inform this class whenever this list changes.
    '''
    def __init__(self, WindowDockReciever, windowList):
        self.windowList = windowList
        self.WindowDockReciever = WindowDockReciever
        for obj in self.windowList:
            self.__callEvent(obj, True)

    def __callEvent(self, windowObj, bind):
        if bind:
            windowObj.bind('move', self.WindowDockReciever._dockingWindowMoveCallback)
        else:
            windowObj.unbind('move', self.WindowDockReciever._dockingWindowMoveCallback)

        self.WindowDockReciever._dockingWindowsUpdateEvent(self)

    def append(self, arg):
        self.__callEvent(arg, True)
        self.windowList.append(arg)

    def __iadd__(self, args):
        for obj in args:
            self.__callEvent(obj, True)
        self.windowList += args
        return self

    def __len__(self):
        return len(self.windowList)

    def remove(self, obj):
        self.__callEvent(obj, False)
        self.windowList.remove(obj)