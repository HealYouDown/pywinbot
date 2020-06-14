from ctypes import windll, POINTER
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, BOOL, POINT, RECT


def PostMessage(
    hWnd: HWND,
    Msg: UINT,
    wParam: WPARAM,
    lParam: LPARAM
) -> bool:
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postmessagea
    func = windll.user32.PostMessageA
    func.argtypes = [HWND, UINT, WPARAM, LPARAM]
    func.restype = BOOL

    res = func(hWnd, Msg, wParam, lParam)
    return bool(res)


def ScreenToClient(
    hWnd: HWND,
    lpPoint: POINTER(POINT),
) -> bool:
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-screentoclient
    func = windll.user32.ScreenToClient
    func.argtypes = [HWND, POINTER(POINT)]
    func.restype = BOOL

    res = func(hWnd, lpPoint)
    return bool(res)


def GetWindowRect(
    hWnd: HWND,
    lpRect: POINTER(RECT)
) -> bool:
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowrect
    func = windll.user32.GetWindowRect
    func.argtypes = [HWND, POINTER(RECT)]
    func.restype = BOOL

    res = func(hWnd, lpRect)
    return bool(res)
