# PyGetWindow

A simple, cross-platform module for obtaining GUI information on and controlling application's windows.

Still under development. Currently only the Windows platform is implemented. If you want to help contribute, please contact al@inventwithpython.com!

## Install

    pip install pygetwindow

## For MacOS

- enable app(Terminal or others) in Privacy & Security > Accessibility

## Examples

(For this example, I'm using Windows and opened the Notepad application, which has a title of "Untitled - Notepad". Most of the effects of these functions can't be seen in text.)

PyGetWindow has functions for obtaining `Window` objects from a place on the screen, from the window title, or just getting all windows. (`hWnd` is specific to the Windows platform.)

    >>> import pygetwindow as gw
    >>> gw.getAllTitles()
    ('', 'C:\\WINDOWS\\system32\\cmd.exe - pipenv  shell - python', 'C:\\github\\PyGetWindow\\README.md • - Sublime Text', "asweigart/PyGetWindow: A simple, cross-platform module for obtaining GUI information on application's windows. - Google Chrome", 'Untitled - Notepad', 'C:\\Users\\Al\\Desktop\\xlibkey.py • - Sublime Text', 'https://tronche.com/gui/x/xlib/ - Google Chrome', 'Xlib Programming Manual: XGetWindowAttributes - Google Chrome', 'Generic Ubuntu Box [Running] - Oracle VM VirtualBox', 'Oracle VM VirtualBox Manager', 'Microsoft Edge', 'Microsoft Edge', 'Microsoft Edge', '', 'Microsoft Edge', 'Settings', 'Settings', 'Microsoft Store', 'Microsoft Store', '', '', 'Backup and Sync', 'Google Hangouts - asweigart@gmail.com', 'Downloads', '', '', 'Program Manager')
    >>> gw.getAllWindows()
    (Win32Window(hWnd=131318), Win32Window(hWnd=1050492), Win32Window(hWnd=67206), Win32Window(hWnd=66754), Win32Window(hWnd=264354), Win32Window(hWnd=329210), Win32Window(hWnd=1114374), Win32Window(hWnd=852550), Win32Window(hWnd=328358), Win32Window(hWnd=66998), Win32Window(hWnd=132508), Win32Window(hWnd=66964), Win32Window(hWnd=66882), Win32Window(hWnd=197282), Win32Window(hWnd=393880), Win32Window(hWnd=66810), Win32Window(hWnd=328466), Win32Window(hWnd=132332), Win32Window(hWnd=262904), Win32Window(hWnd=65962), Win32Window(hWnd=65956), Win32Window(hWnd=197522), Win32Window(hWnd=131944), Win32Window(hWnd=329334), Win32Window(hWnd=395034), Win32Window(hWnd=132928), Win32Window(hWnd=65882))
    >>> gw.getWindowsWithTitle('Untitled')
    (Win32Window(hWnd=264354),)
    >>> gw.getActiveWindow()
    Win32Window(hWnd=1050492)
    >>> gw.getActiveWindow().title
    'C:\\WINDOWS\\system32\\cmd.exe - pipenv  shell - python'
    >>> gw.getWindowsAt(10, 10)
    (Win32Window(hWnd=67206), Win32Window(hWnd=66754), Win32Window(hWnd=329210), Win32Window(hWnd=1114374), Win32Window(hWnd=852550), Win32Window(hWnd=132508), Win32Window(hWnd=66964), Win32Window(hWnd=66882), Win32Window(hWnd=197282), Win32Window(hWnd=393880), Win32Window(hWnd=66810), Win32Window(hWnd=328466), Win32Window(hWnd=395034), Win32Window(hWnd=132928), Win32Window(hWnd=65882))

`Window` objects can be minimized/maximized/restored/activated/resized/moved/closed and also have attributes for their current position, size, and state.

    >>> notepadWindow = gw.getWindowsWithTitle('Untitled')[0]
    >>> notepadWindow.isMaximized
    False
    >>> notepadWindow.maximize()
    >>> notepadWindow.isMaximized
    True
    >>> notepadWindow.restore()
    >>> notepadWindow.minimize()
    >>> notepadWindow.restore()
    >>> notepadWindow.activate()
    >>> notepadWindow.resize(10, 10) # increase by 10, 10
    >>> notepadWindow.resizeTo(100, 100) # set size to 100x100
    >>> notepadWindow.move(10, 10) # move 10 pixels right and 10 down
    >>> notepadWindow.moveTo(10, 10) # move window to 10, 10
    >>> notepadWindow.size
    (132, 100)
    >>> notepadWindow.width
    132
    >>> notepadWindow.height
    100
    >>> notepadWindow.topleft
    (10, 10)
    >>> notepadWindow.top
    10
    >>> notepadWindow.left
    10
    >>> notepadWindow.bottomright
    (142, 110)
    >>> notepadWindow.close()
    >>>

## Support

If you find this project helpful and would like to support its development, [consider donating to its creator on Patreon](https://www.patreon.com/AlSweigart).
