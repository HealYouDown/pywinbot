import time
from typing import List, Union
from ctypes.wintypes import POINT, RECT
from ctypes import byref

from ..memory_reader.helpers import get_process_id
from .functions import PostMessage, GetWindowRect, ScreenToClient
from .keys import VIRTUAL_KEY_CODES as KEYS
from .messages import (WM_CHAR, WM_KEYDOWN, WM_KEYUP, WM_LBUTTONDOWN,
                       WM_LBUTTONUP, WM_RBUTTONDOWN, WM_RBUTTONUP)

KEY_PRESS_DELAY = 0.05


class WindowMessagePoster:
    def __init__(self, hwnd: int):
        self._hwnd = hwnd

    @property
    def hwnd(self) -> int:
        return self._hwnd

    @property
    def window_rect(self) -> RECT:
        rect = RECT()
        GetWindowRect(self.hwnd, byref(rect))
        return rect

    @staticmethod
    def key_names() -> List[str]:
        return list(KEYS.keys())

    @staticmethod
    def by_window(
        window_class: Union[str, None] = None,
        window_title: Union[str, None] = None,
    ) -> "WindowMessagePoster":
        _, hwnd = get_process_id(window_class,
                                 window_title)

        return WindowMessagePoster(hwnd)

    def _keydown(self, key: str) -> None:
        PostMessage(self.hwnd, WM_KEYDOWN, KEYS[key], 0)

    def _keyup(self, key: str) -> None:
        PostMessage(self.hwnd, WM_KEYUP, KEYS[key], 0)

    def _click(self, click_type: str, position: tuple):
        if click_type == "left":
            down_message = WM_LBUTTONDOWN
            up_message = WM_LBUTTONUP
        elif click_type == "right":
            down_message = WM_RBUTTONDOWN
            up_message = WM_RBUTTONUP

        rect = self.window_rect

        # Adjust point to window client area
        point = POINT(rect.left + position[0],
                      rect.top + position[1])
        ScreenToClient(self.hwnd, byref(point))

        pos = point.x | (point.y * 2**16)

        # Post message
        PostMessage(self.hwnd, down_message, 0, pos)
        time.sleep(KEY_PRESS_DELAY)
        PostMessage(self.hwnd, up_message, 0, pos)

    def send_key_press(self, key: str) -> None:
        assert key in WindowMessagePoster.key_names()

        self._keydown(key)
        time.sleep(KEY_PRESS_DELAY)
        self._keyup(key)

    def send_enter(self) -> None:
        self.send_key_press("enter")

    def send_char(self, char: str) -> None:
        PostMessage(self.hwnd, WM_CHAR, ord(char), 0)

    def send_string(self, string: str) -> None:
        for char in string:
            self.send_char(char)

    def send_left_click(self, position: tuple) -> None:
        self._click("left", position)

    def send_right_click(self, position: tuple) -> None:
        self._click("right", position)
