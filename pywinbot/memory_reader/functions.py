from ctypes import POINTER, c_size_t, windll
from ctypes.wintypes import (BOOL, DWORD, HANDLE, HWND, LPCSTR, LPCVOID,
                             LPDWORD, LPVOID)
from typing import Union

from .structures import MODULEENTRY32


def OpenProcess(
    dwDesiredAccess: DWORD,
    bInheritHandle: BOOL,
    dwProcessId: DWORD,
) -> Union[HANDLE, None]:
    # https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess
    func = windll.kernel32.OpenProcess
    func.argtypes = [DWORD, BOOL, DWORD]
    func.restype = HANDLE

    return func(dwDesiredAccess, bInheritHandle, dwProcessId)


def ReadProcessMemory(
    hProcess: HANDLE,
    lpBaseAddress: LPCVOID,
    lpBuffer: LPVOID,
    nSize: c_size_t,
    lpNumberOfBytesRead: POINTER(c_size_t),
) -> bool:
    # https://docs.microsoft.com/de-de/windows/win32/api/memoryapi/nf-memoryapi-readprocessmemory
    func = windll.kernel32.ReadProcessMemory
    func.argtypes = [HANDLE, LPCVOID, LPVOID, c_size_t, POINTER(c_size_t)]
    func.restype = BOOL

    res = func(hProcess, lpBaseAddress, lpBuffer, nSize, lpNumberOfBytesRead)
    return bool(res)


def WriteProcessMemory(
    hProcess: HANDLE,
    lpBaseAddress: LPCVOID,
    lpBuffer: LPCVOID,
    nSize: c_size_t,
    lpNumberOfBytesWritten: POINTER(c_size_t)
) -> bool:
    # https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory
    func = windll.kernel32.WriteProcessMemory
    func.argtypes = [HANDLE, LPCVOID, LPVOID, c_size_t, POINTER(c_size_t)]
    func.restype = BOOL

    res = func(hProcess, lpBaseAddress, lpBuffer, nSize,
               lpNumberOfBytesWritten)
    return bool(res)


def CloseHandle(
    hObject: HANDLE
) -> bool:
    # https://docs.microsoft.com/de-de/windows/win32/api/handleapi/nf-handleapi-closehandle
    func = windll.kernel32.CloseHandle
    func.argtypes = [HANDLE]
    func.restype = BOOL

    res = func(hObject)
    return bool(res)


def CreateToolhelp32Snapshot(
    dwFlags: DWORD,
    th32ProcessID: DWORD,
) -> HANDLE:
    # https://docs.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot
    func = windll.kernel32.CreateToolhelp32Snapshot
    func.argtypes = [DWORD, DWORD]
    func.restype = HANDLE

    return func(dwFlags, th32ProcessID)


def Module32First(
    hSnapshot: HANDLE,
    lpme: POINTER(MODULEENTRY32)
) -> bool:
    # https://docs.microsoft.com/de-de/windows/win32/api/tlhelp32/nf-tlhelp32-module32first
    func = windll.kernel32.Module32First
    func.argtypes = [HANDLE, POINTER(MODULEENTRY32)]
    func.restypes = BOOL

    res = func(hSnapshot, lpme)
    return bool(res)


def Module32Next(
    hSnapshot: HANDLE,
    lpme: POINTER(MODULEENTRY32)
) -> bool:
    # https://docs.microsoft.com/de-de/windows/win32/api/tlhelp32/nf-tlhelp32-module32next
    func = windll.kernel32.Module32First
    func.argtypes = [HANDLE, POINTER(MODULEENTRY32)]
    func.restypes = BOOL

    res = func(hSnapshot, lpme)
    return bool(res)


def FindWindow(
    lpClassName: LPCSTR,
    lpWindowName: LPCSTR,
) -> Union[HWND, None]:
    # https://docs.microsoft.com/de-de/windows/win32/api/winuser/nf-winuser-findwindowa
    func = windll.user32.FindWindowA
    func.argtypes = [LPCSTR, LPCSTR]
    func.restypes = HWND

    res = func(lpClassName, lpWindowName)
    if res == 0:
        return None
    return res


def GetWindowThreadProcessId(
    hWnd: HWND,
    lpdwProcessId: LPDWORD
) -> DWORD:
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowthreadprocessid
    func = windll.user32.GetWindowThreadProcessId
    func.argtypes = [HWND, LPDWORD]
    func.restypes = DWORD

    return func(hWnd, lpdwProcessId)
