from ctypes import byref
from ctypes.wintypes import POINT, RECT
from time import sleep
from typing import Tuple

from .functions import GetWindowRect, PostMessage, ScreenToClient
from .keys import VK_CODE
from .messages import (WM_CHAR, WM_KEYDOWN, WM_KEYUP, WM_LBUTTONDOWN,
                       WM_LBUTTONUP, WM_RBUTTONDOWN, WM_RBUTTONUP)

KEY_DOWN_UP_SLEEP = 0.1


class WindowMessagePoster:
    def __init__(self, hwnd: int):
        self._hwnd = hwnd

    @property
    def hwnd(self)-> int:
        return self._hwnd

    def get_rect(self) -> RECT:
        """Returns the rect of the registered handle.
        Rect has left, top right, bottom attributes."""
        rect = RECT()
        GetWindowRect(self.hwnd, byref(rect))
        return rect

    def hold_key(self, key: str) -> None:
        PostMessage(self.hwnd, WM_KEYDOWN, VK_CODE[key], 0)

    def release_key(self, key: str) -> None:
        PostMessage(self.hwnd, WM_KEYUP, VK_CODE[key], 0)

    def send_enter(self) -> None:
        """Sends enter event to window."""
        PostMessage(self.hwnd, WM_KEYDOWN, VK_CODE["enter"], 0)
        sleep(KEY_DOWN_UP_SLEEP)
        PostMessage(self.hwnd, WM_KEYUP, VK_CODE["enter"], 0)

    def send_char(self, char: str) -> None:
        """Sends a single char to window."""
        PostMessage(self.hwnd, WM_CHAR, ord(char), 0)

    def send_string(self, string: str) -> None:
        """Sends a string to window."""
        for char in string:
            self.send_char(char)

    def send_key(self, key: str) -> None:
        """Sends key input to window."""
        PostMessage(self.hwnd, WM_KEYDOWN, VK_CODE[key], 0)
        sleep(KEY_DOWN_UP_SLEEP)
        PostMessage(self.hwnd, WM_KEYUP, VK_CODE[key], 0)

    def send_left_click(self, pos: tuple) -> None:
        """Sends a left click to in-window coordinates..
        (100, 100) would be (window_position_x + 100, window_position_y + 100). Basically
        adjusts for screen movement"""
        rect = self.get_rect()
        
        point = POINT(rect.left + pos[0],
                      rect.top + pos[1])
        ScreenToClient(self.hwnd, byref(point))

        shifted_pos = point.x | (point.y << 16)

        PostMessage(self.hwnd, WM_LBUTTONDOWN, 0, shifted_pos)
        sleep(KEY_DOWN_UP_SLEEP)
        PostMessage(self.hwnd, WM_LBUTTONUP, 0, shifted_pos)

    def send_right_click(self, pos: tuple) -> None:
        """Sends a right click to in-window coordinates..
        (100, 100) would be (window_position_x + 100, window_position_y + 100). Basically
        adjusts for screen movement"""
        rect = self.get_rect()
        
        point = POINT(rect.left + pos[0],
                      rect.top + pos[1])
        ScreenToClient(self.hwnd, byref(point))

        shifted_pos = point.x | (point.y << 16)

        PostMessage(self.hwnd, WM_RBUTTONDOWN, 0, shifted_pos)
        sleep(KEY_DOWN_UP_SLEEP)
        PostMessage(self.hwnd, WM_RBUTTONUP, 0, shifted_pos)
