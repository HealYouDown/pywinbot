# Pywinbot
This library aims at providing a basic interface to some winapi calls to write scripts / bots for certain tasks.

## MemoryReader
Using the `MemoryReader` class, one can read / rewrite the memory of a process.

### Example
> Addresses used are not the actual addresses in Notepad

Let's assume we want to read the content of the Windows Notepad, which for this example has a length of 20 characters.
```py
from pywinbot_core import MemoryReader, Address

mr = MemoryReader(window_class="Notepad")
addr = Address("ABC12345DEF")
content = mr.read(addr, "str", 20)
```
If the address to be read/write from is offset from our address above, you can calculate the address the following way.
```py
mr = MemoryReader(...)
addr = mr.get_final_pointer("ABC12345DEF", offsets=["40", "20A"])
content = mr.read(addr, "str", 20)
```
Now we want to change the content in the Notepad.
```py
mr = MemoryReader(...)
to_write = "Foobarspamegg"
mr.write(addr, to_write, len(to_write))
```

## WindowMessagePoster
The `WindowMessagePoster` allows to send keyboard and mouse events to a specific window in the background.
> The window does not need to have focus or be in the foreground. However, it is not allowed to be minimized.

### Example
```py
from pywinbot_core import WindowMessagePoster
# If we previously used our MemoryReader class for Notepad, we can initalize the class the following way.
wmp = WindowMessagePoster(mr.hwnd)

# If you just want to use the WindowMessagePoster, you can initalize the class like below.
wmp = WindowMessagePoster.by_window(window_class="Notepad")
```
We can now send keyboard or mouse events to the window.
```py
# Left clicks at 100, 200 inside the window. The position is offset by the top left corner of the window.
wmp.send_left_click(100, 200)

# Presses enter
wmp.send_enter()

# Writes a string
wmp.send_string("Foobarspamegg")

# You can also send different keyboard events like arrow keys, function keys, ...
wmp.send_key_press("f1")
wmp.send_key_press("esc")
```
You can get a list with all available keys the following way.
```py
>>> WindowMessagePoster.key_names()
```

## License
[MIT License](https://opensource.org/licenses/MIT)