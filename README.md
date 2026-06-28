# Pynus

<div align="center"><img src="images/Pynus.png" width="200"></div>

Pynus is a Python library for creating menu-based CLI applications. It provides an intuitive way to structure menus using a stack-based navigation system, with colorful terminal rendering powered by [`RainbowPicker`](https://github.com/GBiondo1310/rainbow_pick.git).

## Features

- **Stack-based navigation** — naturally handles Back, forward, and nested menus
- **Decorator-driven callbacks** — bind actions to menu options with `@callback`
- **Single and multi-select** — built-in support for both modes
- **Yes/No menu** — ready-to-use `PynusYN` class
- **Colorful UI** — leverages RainbowPicker for colored terminal rendering
- **Safe navigation** — "Back" option is automatically appended to single-select menus

## Installation

**pip:**
```sh
pip install pynus@git+"https://github.com/GBiondo1310/Pynus.git"
```

**uv:**
```sh
uv add https://github.com/GBiondo1310/Pynus.git"
```

Requires Python ≥ 3.12.

---

## Quick Start

```python
from pynus import PynusBase, callback

class GreetingMenu(PynusBase):
    def __init__(self):
        super().__init__("Pick a greeting", ["Hello", "Goodbye"])
        self.init_callbacks()

    def init_callbacks(self):
        @callback(self, index=0)
        def say_hello(**kwargs):
            print("👋 Hello there!")
            return self  # Stay on this menu

        @callback(self, index=1)
        def say_goodbye(**kwargs):
            print("👋 See you!")
            # Returning None exits

menu = GreetingMenu()
menu.start()
```

Run it and navigate with the arrow keys. Press **Enter** to select, or pick **Back** to return.

---

## Core Concepts

### PynusBase

`PynusBase` is the base class for all menus. It extends `RainbowPicker` and adds callback registration, automatic "Back" option handling, and navigation support.

```python
class PynusBase(RainbowPicker):
    def __init__(self, title: str, options: list[object], *, include_back: bool = True, **kwargs)
```

- **`title`** — the menu title displayed at the top
- **`options`** — list of choices (strings or objects)
- **`include_back`** — automatically append a "Back" option (default: `True`). Set to `False` for menus that don't need it (multiselect does this automatically)
- **`**kwargs`** — forwarded to `RainbowPicker` (e.g. `multiselect`, `indicator`, `clear_screen`)

### The `@callback` decorator

The `@callback` decorator binds a function to a menu option. It can match by **index**, by **option value (obj)**, or as a catch-all **"all"** handler.

```python
from pynus import PynusBase, callback

menu = PynusBase("Settings", ["Theme", "Sound", "About"])

# Match by index — fires when the first option ("Theme") is selected
@callback(menu, index=0)
def theme_handler(**kwargs):
    print(f"You picked: {kwargs['instance']} (index {kwargs['index']})")
    # Return a new menu or None to go back

# Match by option value — fires when "Sound" is selected
@callback(menu, obj="Sound")
def sound_handler(**kwargs):
    print("Sound settings")
    return self  # Re-show this menu

# Catch-all — runs for every selection (side effects first)
@callback(menu)
def log_selection(**kwargs):
    print(f"Selected: {kwargs['instance']}")
```

**Dispatch order:**
1. The **"all"** callback runs first (for side effects like logging)
2. A **specific** callback (by index or obj) runs next — its return value is used
3. If no specific callback matches, the **"all"** callback's return value is used as fallback

### Callback return values

What your callback returns controls navigation:

| Return value | Behavior |
|---|---|
| A new menu object | Mainloop switches to that menu |
| `self` | Current menu re-displays |
| `None` | Goes back to the previous menu (from stack) |

---

## PynusYN — Yes / No Menu

A built-in menu that returns `True` for Yes and `False` for No:

```python
from pynus import PynusYN

yn = PynusYN("Continue?")
result = yn.start()

if result is True:
    print("User said Yes")
elif result is False:
    print("User said No")
else:
    print("User picked Back")
```

---

## PynusMultiselect — Multi-Selection

`PynusMultiselect` lets users pick multiple options (using **Space** to toggle, **Enter** to confirm). It does **not** include a "Back" option.

```python
from pynus import PynusMultiselect, callback

class ToppingMenu(PynusMultiselect):
    def __init__(self):
        super().__init__("Choose toppings", ["Cheese", "Pepperoni", "Mushrooms", "Olives"])
        self.init_callbacks()

    def init_callbacks(self):
        @callback(self)
        def log_topping(**kwargs):
            print(f"  → Selected: {kwargs['instance']}")

menu = ToppingMenu()
selections = menu.start()
print(f"\nFinal selections: {selections}")
```

Returns a list of `(option_text, index)` tuples, or `None` if nothing was selected.

---

## Stack Navigation

The `Stack` class manages menu history. Use `stack.push()` to save the current menu before navigating to a new one, and `stack.mainloop()` to run the navigation loop.

### How it works

```
User sees Menu A → picks an option
  → callback pushes Menu A to stack and returns Menu B
  → mainloop displays Menu B
  → user picks "Back" (or callback returns None)
  → mainloop pops Menu A from stack and shows it
```

### Complete example

```python
from __future__ import annotations
from pynus import PynusBase, PynusYN, stack, callback


class MainMenu(PynusBase):
    def __init__(self):
        super().__init__("Main Menu", ["Play Game", "Settings", "Quit"])
        self.init_callbacks()

    def init_callbacks(self):
        @callback(self, index=0)
        def play(**kwargs):
            stack.push(self)          # Save MainMenu to stack
            return GameMenu()

        @callback(self, index=1)
        def settings(**kwargs):
            stack.push(self)
            return SettingsMenu()

        @callback(self, index=2)
        def quit(**kwargs):
            yn = PynusYN("Are you sure?")
            result = yn.start()
            if result is True:
                return None           # Exit the loop
            return self               # Stay on main menu


class GameMenu(PynusBase):
    def __init__(self):
        super().__init__("Game Menu", ["New Game", "Load Game"])
        self.init_callbacks()

    def init_callbacks(self):
        @callback(self, index=0)
        def new_game(**kwargs):
            print("🎮 Starting new game...")
            return self

        @callback(self, index=1)
        def load_game(**kwargs):
            print("💾 Loading game...")
            return self

        # "Back" returns None automatically → pops MainMenu from stack


class SettingsMenu(PynusBase):
    def __init__(self):
        super().__init__("Settings", ["Volume", "Brightness"])
        self.init_callbacks()

    def init_callbacks(self):
        @callback(self, index=0)
        def volume(**kwargs):
            print("🔊 Volume settings")
            return self

        @callback(self, index=1)
        def brightness(**kwargs):
            print("☀️  Brightness settings")
            return self


stack.push(MainMenu())   # Start with MainMenu
stack.mainloop()         # Run the navigation loop
```

### Stack API

| Method | Description |
|---|---|
| `push(menu)` | Save a menu to the history stack |
| `pop()` | Retrieve the last menu (returns `None` if empty) |
| `mainloop()` | Start the navigation loop |
| `pop(index)` | Retrieve a menu at a specific position (0 = bottom) |

The default `stack` instance is already created for you. You can also create your own:

```python
from pynus import Stack

my_stack = Stack()
my_stack.push(MainMenu())
my_stack.mainloop()
```

---

## Advanced: Nested callbacks & patterns

### Using "all" callback for side effects

The "all" callback runs for every selection before the specific callback. This is useful for logging, validation, or shared setup:

```python
class LoggedMenu(PynusBase):
    def __init__(self):
        super().__init__("Menu", ["A", "B"])
        self.init_callbacks()

    def init_callbacks(self):
        @callback(self)             # Runs for every selection
        def log(**kwargs):
            print(f"[LOG] Option {kwargs['index']} selected")

        @callback(self, index=0)    # Runs after log()
        def option_a(**kwargs):
            print("Handling A")
            return MenuB()

        @callback(self, index=1)
        def option_b(**kwargs):
            print("Handling B")
```

### Registering callbacks after initialization

Callbacks don't have to be defined inside the class — you can register them on an existing instance:

```python
menu = PynusBase("Menu", ["Save", "Delete"])

@callback(menu, index=0)
def save(**kwargs):
    print("Saving...")
    return self
```

---

## API Reference

### `pynus` module exports

| Name | Description |
|---|---|
| `PynusBase` | Base class for single-select menus |
| `PynusMultiselect` | Class for multi-select menus |
| `PynusYN` | Yes/No menu returning `True`/`False` |
| `Stack` | Stack class for menu navigation |
| `stack` | Default Stack instance |
| `callback` | Decorator to register menu callbacks (`PynusBase.add_callback`) |

### `PynusBase`

```python
class PynusBase(
    title: str,
    options: list[object],
    *,
    include_back: bool = True,
    **kwargs
)
```

**Methods:**
- `start()` — display the menu and return the callback result
- `callback(**kwargs)` — dispatch to registered callbacks

**Attributes:**
- `callbacks` — dictionary of registered callback functions

### `PynusMultiselect`

```python
class PynusMultiselect(
    title: str,
    options: list[object],
    **kwargs
)
```

**Methods:**
- `start()` — display the menu and return a list of `(option, index)` tuples, or `None`

### `PynusYN`

```python
class PynusYN(title: str)
```

**Returns:** `True` (Yes), `False` (No), or `None` (Back)

### `Stack`

```python
class Stack()
```

**Methods:**
- `push(object)` — add an item to the stack
- `pop(index=-1)` — remove and return an item (returns `None` if empty)
- `mainloop()` — run the navigation loop

---

## License

MIT License
