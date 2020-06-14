from ctypes import addressof, byref, sizeof
from ctypes.wintypes import DWORD, LPCSTR
from typing import Tuple

from .address import Address
from .flags import TH32CS_SNAPMODULE, TH32CS_SNAPMODULE32
from .functions import (CloseHandle, CreateToolhelp32Snapshot, FindWindow,
                        GetWindowThreadProcessId, Module32First, Module32Next)
from .structures import MODULEENTRY32


def get_module_offset(
    process_id: int,
    process_name: str
) -> Address:
    """Returns an Adress with the base offset of the process.

    Args:
        process_id (int): PID
        process_name (str): Name of the process. Case does not matter.

    Returns:
        Address: Adress with the base offset of the process.
    """

    flag = TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32
    snap = CreateToolhelp32Snapshot(flag, process_id)

    me32 = MODULEENTRY32()
    me32.dwSize = sizeof(MODULEENTRY32)

    Module32First(snap, byref(me32))
    while True:
        name = me32.szModule.decode("ascii")
        if process_name.lower() in name.lower():
            base_addr = me32.modBaseAddr
            addr = Address(addressof(base_addr.contents))

            CloseHandle(snap)

            return addr

        if not Module32Next(snap, byref(me32)):
            break

    CloseHandle(snap)


def get_process_id(
    window_class: str = None,
    window_title: str = None,
) -> Tuple[int, int]:
    """Gets process ID by finding the window either via
    its class or title.

    Args:
        window_class (str, optional): Window class
        window_title (str, optional): Window title

    Returns:
        Tuple[int, int]: PID, HWND
    """

    try:
        arg1 = LPCSTR(window_class.encode("utf-8"))
    except AttributeError:
        arg1 = None

    try:
        arg2 = LPCSTR(window_title.encode("utf-8"))
    except AttributeError:
        arg2 = None

    hwnd = FindWindow(arg1, arg2)

    pid = DWORD()
    GetWindowThreadProcessId(hwnd, byref(pid))

    return pid.value, hwnd
