import Quartz
import pygetwindow
from AppKit import (
    NSWorkspace,
    NSRunningApplication,
    NSApplicationActivateIgnoringOtherApps,
)
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID,
    kCGWindowListExcludeDesktopElements,
    kCGWindowLayer,
    kCGWindowBounds,
    kCGWindowOwnerPID,
    kCGWindowOwnerName,
    kCGWindowName,
)
from HIServices import (
    AXUIElementCreateApplication,
    AXUIElementCopyAttributeValue,
    AXUIElementSetAttributeValue,
    AXUIElementPerformAction,
    AXValueCreate,
    AXValueGetValue,
    kAXWindowsAttribute,
    kAXPositionAttribute,
    kAXSizeAttribute,
    kAXTitleAttribute,
    kAXCloseButtonAttribute,
    kAXMinimizedAttribute,
    kAXPressAction,
    kAXValueTypeCGPoint,
    kAXValueCGSizeType,
)


def _formatFullTitle(window):
    return "%s %s" % (window.get(kCGWindowOwnerName, ""), window.get(kCGWindowName, ""))


def getAllTitles():
    """Returns a list of strings of window titles for all visible windows."""
    windows = CGWindowListCopyWindowInfo(
        kCGWindowListOptionOnScreenOnly | kCGWindowListExcludeDesktopElements,
        kCGNullWindowID,
    )
    return [_formatFullTitle(win) for win in windows]


def getActiveWindow():
    """Returns a Window object of the currently active Window."""
    windows = CGWindowListCopyWindowInfo(
        kCGWindowListOptionOnScreenOnly | kCGWindowListExcludeDesktopElements,
        kCGNullWindowID,
    )
    for win in windows:
        if win.get(kCGWindowLayer) == 0:
            return MacOSWindow(win)
    return None


def getWindowsAt(x, y):
    windows = CGWindowListCopyWindowInfo(
        kCGWindowListOptionOnScreenOnly | kCGWindowListExcludeDesktopElements,
        kCGNullWindowID,
    )
    matches = []
    for win in windows:
        bounds = win[kCGWindowBounds]
        if pygetwindow.pointInRect(
            x, y, bounds["X"], bounds["Y"], bounds["Width"], bounds["Height"]
        ):
            matches.append(MacOSWindow(win))
    return matches


def getWindowsWithTitle(title):
    """Returns a list of Window objects that substring match ``title`` in their title text."""

    windows = CGWindowListCopyWindowInfo(
        kCGWindowListOptionOnScreenOnly | kCGWindowListExcludeDesktopElements,
        kCGNullWindowID,
    )
    matches = []
    for win in windows:
        full_title = _formatFullTitle(win)
        if title.upper() in full_title.upper():
            matches.append(MacOSWindow(win))
    return matches


def getAllWindows():
    """Returns a list of Window objects for all visible windows."""
    windows = CGWindowListCopyWindowInfo(
        kCGWindowListOptionOnScreenOnly | kCGWindowListExcludeDesktopElements,
        kCGNullWindowID,
    )
    return [MacOSWindow(win) for win in windows]


class MacOSApp:
    def __init__(self, pid):
        self._pid = pid
        self._app = AXUIElementCreateApplication(self._pid)

    def getWindow(self, windowTitle):
        _, windows = AXUIElementCopyAttributeValue(self._app, kAXWindowsAttribute, None)
        if windows:
            for w in windows:
                _, title = AXUIElementCopyAttributeValue(w, kAXTitleAttribute, None)
                if title == windowTitle:
                    return w
        return None


class MacOSWindow(pygetwindow.BaseWindow):
    def __init__(self, win):
        self._win = win
        self._window_title = win.get(kCGWindowName)
        self._full_title = _formatFullTitle(win)

        self._pid = win[kCGWindowOwnerPID]
        self._app = MacOSApp(self._pid)
        self._setupRectProperties()

        bounds = win[kCGWindowBounds]
        self._init_react = pygetwindow.Rect(
            bounds["X"],
            bounds["Y"],
            bounds["X"] + bounds["Width"],
            bounds["Y"] + bounds["Height"],
        )
        self._maximize_rect = None

    def _getWindow(self):
        return self._app.getWindow(self._window_title)

    def _getWindowSize(self, window):
        _, size = AXUIElementCopyAttributeValue(window, kAXSizeAttribute, None)
        _, res = AXValueGetValue(size, kAXValueCGSizeType, None)
        return res

    def _getWindowPos(self, window):
        _, pos = AXUIElementCopyAttributeValue(window, kAXPositionAttribute, None)
        _, res = AXValueGetValue(pos, kAXValueTypeCGPoint, None)
        return res

    def _getWindowRect(self):
        window = self._getWindow()
        if not window:
            return self._init_react
        size = self._getWindowSize(window)
        pos = self._getWindowPos(window)
        return pygetwindow.Rect(pos.x, pos.y, pos.x + size.width, pos.y + size.height)

    def _getScreenRect(self):
        main_display = Quartz.CGMainDisplayID()
        screen_rect = Quartz.CGDisplayBounds(main_display)
        return pygetwindow.pyrect.Rect(
            screen_rect.origin.x,
            screen_rect.origin.y,
            screen_rect.size.width,
            screen_rect.size.height,
        )

    def _setWindowSize(self, window, size):
        """
        size = (newWidth, newHeight)
        """
        size_ref = AXValueCreate(kAXValueCGSizeType, size)
        AXUIElementSetAttributeValue(window, kAXSizeAttribute, size_ref)

    def _setWindowPos(self, window, pos):
        """
        pos = (newLeft, newTop)
        """
        pos_ref = AXValueCreate(kAXValueTypeCGPoint, pos)
        AXUIElementSetAttributeValue(window, kAXPositionAttribute, pos_ref)

    def close(self):
        window = self._getWindow()
        if window:
            _, close_button = AXUIElementCopyAttributeValue(
                window, kAXCloseButtonAttribute, None
            )
            if close_button:
                AXUIElementPerformAction(close_button, kAXPressAction)

    def minimize(self):
        window = self._getWindow()
        if window:
            AXUIElementSetAttributeValue(window, kAXMinimizedAttribute, True)

    def deminimize(self):
        window = self._getWindow()
        if window:
            AXUIElementSetAttributeValue(window, kAXMinimizedAttribute, False)

    def maximize(self):
        screen_rect = self._getScreenRect()
        self.moveTo(screen_rect.left, screen_rect.top)
        self.resizeTo(screen_rect.width, screen_rect.height)
        self._maximize_rect = self._getWindowRect()

    def restore(self):
        if self.isMinimized:
            self.deminimize()
        else:
            self.moveTo(self._init_react.left, self._init_react.top)
            self.resizeTo(
                self._init_react.right - self._init_react.left,
                self._init_react.bottom - self._init_react.top,
            )

    def activate(self):
        app = NSRunningApplication.runningApplicationWithProcessIdentifier_(
            self._win[kCGWindowOwnerPID]
        )
        if app:
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)

    def resizeRel(self, widthOffset, heightOffset):
        self.resizeTo(self.width + widthOffset, self.height + heightOffset)

    def resizeTo(self, newWidth, newHeight):
        window = self._getWindow()
        if window:
            self._setWindowSize(window, (newWidth, newHeight))

    def moveRel(self, xOffset, yOffset):
        self.moveTo(self.left + xOffset, self.top + yOffset)

    def moveTo(self, newLeft, newTop):
        window = self._getWindow()
        if window:
            self._setWindowPos(window, (newLeft, newTop))

    @property
    def isMinimized(self):
        window = self._getWindow()
        if window:
            ok, minimized = AXUIElementCopyAttributeValue(
                window, kAXMinimizedAttribute, None
            )
            return minimized
        return False

    @property
    def isMaximized(self):
        if self._maximize_rect is not None:
            return self._maximize_rect == self._getWindowRect()
        return False

    @property
    def title(self):
        return self._full_title
