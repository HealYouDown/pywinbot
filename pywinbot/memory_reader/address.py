from typing import Union


class Address:
    """A class used to easier represent memory addresses.

    To use:
    >>> addr = Address("10BC4AF0")
    <Address hex=10BC4AF0 decimal=280775408>

    Calculating:
    >>> addr += 4
    <Address hex=10BC4AF4 decimal=280775412>
    >>> addr += "A"
    <Address hex=10BC4AFE decimal=280775422>
    >>> addr += Address("10BA0170")
    <Address hex=21764C6E decimal=561400942>
    """
    def __init__(self, address: Union[int, str]):
        """Initalizes Address class.

        Args:
            address (Union[int, str]): the address either as a string
                or as an integer.
        """
        if isinstance(address, str):
            self.address_string = address
            self.address_decimal = int(address, 16)

        elif isinstance(address, int):
            self.address_string = hex(address)
            self.address_decimal = address

    def __repr__(self) -> str:
        # Formats 0x10bc4af0 to 10BC4AF0
        string = self.address_string.replace("0x", "").upper()
        return f"<Address hex={string} decimal={self.address_decimal}>"

    def __add__(self, other: Union["Address", str, int]) -> "Address":
        if isinstance(other, str):
            return Address(self.address_decimal + int(other, 16))

        elif isinstance(other, int):
            return Address(self.address_decimal + other)

        elif isinstance(other, Address):
            return Address(self.address_decimal + other.address_decimal)

    def __mul__(self, other: int):
        return Address(self.address_decimal * other)
