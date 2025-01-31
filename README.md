# Pynus

<div align="center"><img src="images/Pynus.png" width="200"></div>

Pynus is a Python library for creating menu-based CLI applications. It provides an intuitive way to structure menus using a stack-based approach while leveraging colored selections with `RainbowPicker`.

## Features
- Easy-to-use menu system with stack-based navigation.
- Supports customizable options and callback functions.
- Simple decorator-based input matching.
- Integrated with [`RainbowPicker`](https://github.com/GBiondo1310/rainbow_pick.git) for colored selections.

## Installation

Using ```pip```
```sh
pip install pynus@git+"https://github.com/GBiondo1310/Pynus.git"
```

Using ```uv```
```sh
uv add https://github.com/GBiondo1310/Pynus.git
```

## Usage

### Creating Menus

```python
from pynus import PynusBase, Stack

class MainMenu(PynusBase):
    def __init__(self):
        super().__init__("Main Menu", ["Go to SubMenu", "Exit"])

    @PynusBase.match_input(index=0)
    def go_to_submenu(self):
        stack += self
        return SubMenu()
        
class SubMenu(PynusBase):
    def __init__(self):
        super().__init__("Sub Menu", ["Option A", "Option B", "Back"])

    @PynusBase.match_input(index=0)
    def option_a(self):
        print("You chose Option A")
        return None

    @PynusBase.match_input(index=1)
    def option_b(self):
        print("You chose Option B")
        return None

if __name__ == "__main__":
    stack = Stack()
    stack += MainMenu()
    stack.main_loop()
```

## How It Works

The ```PynusBase.match_input``` decorator allows to define functions to be called
on user's choice.
The user's choice can be matched by index or by object, this allows the flexibility to
work with both.

## Example Output
```
Main Menu
1. Go to SubMenu
2. Exit
Select an option: 1

Sub Menu
1. Option A
2. Option B
3. Back
Select an option: 1
You chose Option A
```

## License
MIT License

