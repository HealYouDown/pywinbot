import re
import struct
from ctypes import create_string_buffer
from struct import unpack
from typing import List, Union

from .flags import PROCESS_VM_OPERATION, PROCESS_VM_READ, PROCESS_VM_WRITE
from .address import Address
from .functions import (CloseHandle, OpenProcess, ReadProcessMemory,
                        WriteProcessMemory)
from .helpers import get_module_offset, get_process_id


class MemoryReader:
    def __init__(
        self,
        process_name: str,
        window_class: Union[str, None] = None,
        window_title: Union[str, None] = None,
    ):
        """Class to read or write memory from a process.

        Args:
            process_name (str): Name of the process (e.g. Notepad.exe).
                Case does not matter.
            window_class (Union[str, None], optional): Window Class of
                the process you want to read memory from. If not given,
                window_title has to be not None.
            window_title (Union[str, None], optional): Window Title of
                the process you want to read memory from. If not given,
                window_class has to be not None.

        To use:
        >>> mr = MemoryReader(process_name="Notepad.exe",
                              window_class="Notepad")
        """

        self._pid, self._hwnd = get_process_id(window_class,
                                               window_title)

        # Process was not found
        if self.pid == 0 and self.hwnd is None:
            raise Exception("Process was not found.")

        self._module_offset = get_module_offset(self.pid,
                                                process_name)

        flags = PROCESS_VM_READ | PROCESS_VM_OPERATION | PROCESS_VM_WRITE
        self._process_handle = OpenProcess(flags, False, self.pid)

    @property
    def pid(self) -> int:
        """Returns the process ID (PID) for the found process

        Returns:
            int: PID
        """
        return self._pid

    @property
    def hwnd(self) -> int:
        """Returns the Window Handle for found process.

        Returns:
            int: Window Handle
        """
        return self._hwnd

    def get_final_pointer(
        self,
        base_pointer_addr: Union[Address, str],
        offsets: List[str]
    ) -> Address:
        """Calculates the address based on offsets and base pointer
        given.

        Args:
            base_pointer_addr (Union[Address, str]): The base pointer address.
            offsets (List[str]): The offsets given in a list of strings.
                Order does matter.

        Returns:
            Address: returns a new Address that points to the value
                of the base pointer and given offsets.

        To use:
        >>> mr = MemoryReader(...)
        >>> base_addr = Address("ABC123456")
        >>> base_pointer = mr.get_final_pointer(base_addr,
                                                offsets=["40", "F08"])
        You can now read/write the memory at this pointer position
        >>> value = mr.read(base_pointer, ...)
        """

        addr = self._module_offset + base_pointer_addr

        for index, offset in enumerate(offsets):
            addr2 = Address(self.read(addr,
                                      "i",
                                      4))

            if index == len(offsets)-1:
                return addr2 + offsets[-1]
            else:
                addr = addr2 + offset

    def close(self):
        """Closes the process handle."""
        CloseHandle(self._process_handle)

    def read(
        self,
        address: Address,
        unpack_type: str,
        buffer_size: int
    ) -> Union[str, int, float, None]:
        """Reads the process memory from given address.

        Args:
            address (Address): The address to read from.
            unpack_type (str): The data type to unpack. For strings,
                use 'str', integer 'i', float 'f', ... (See struct unpacks).
            buffer_size (int): the size of the data to read.

        Returns:
            Union[str, int, float, None]: returns result based on unpack_type.
                Will return None if reading failed.

        To use:
        >>> mr = MemoryReader(...)
        >>> addr = Address("ABC123456")
        >>> # We assume that at ABC123456 there is a 4-byte integer stored
        >>> value = mr.read(addr, "i", 4)
        """

        buffer = create_string_buffer(buffer_size)

        if ReadProcessMemory(self._process_handle,
                             address.address_decimal,
                             buffer,
                             buffer_size,
                             None):

            if unpack_type == "str":
                string = buffer.raw.decode("utf-8", errors="ignore")
                return re.sub(r"[^A-Za-z0-9]+", "", string)
            else:
                return unpack(unpack_type, buffer.raw)[0]

        return None

    def write(
        self,
        address: Address,
        value: Union[int, float, str],
        buffer_size: int
    ) -> bool:
        """Writes data in the process' memory at given address.

        Args:
            address (Address): The address to write to.
            value (Union[int, float, str]): the data that is
                written to the memory.
            buffer_size (int): the size of the data written to.

        Returns:
            bool: True means success, False means writing failed.

        To use:
        >>> mr = MemoryReader(...)
        >>> addr = Address("ABC123456")
        >>> to_write = "foobar"
        >>> mr.write(addr, to_write, len(to_write))
        """
        if isinstance(value, str):
            buffer = create_string_buffer(bytes(value, "ascii"),
                                          buffer_size)

        elif isinstance(value, float):
            buffer = create_string_buffer(struct.pack("f", value),
                                          buffer_size)

        elif isinstance(value, int):
            buffer = create_string_buffer(struct.pack("i", value),
                                          buffer_size)

        return WriteProcessMemory(self._process_handle,
                                  address.address_decimal,
                                  buffer,
                                  buffer_size,
                                  None)
