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

## Concepts

- ### PynusBase
The main class of the library and all the new menus **must** inherit from this class.

#### Matching user's choices:
A convenient decorator is provided by the library: ``@PynusBase.add_callback`` or ``@callback``

##### How to use it:
```python
from pynus import PynusBase, callback

class MainMenu(PynusBase):
    def __init__(self):
        super().__init__(
            title = "This is a test menu",
            options = ["Option 1", "Option 2"]
        )

        #: Callbacks can be defined directly in the __init__ function passing self as first arg
        @callback(self, index=0) #: index = 0 will match first option
        def option_1(**kwargs): 
            #: **kwargs is mandatory as index and instance will be passed in order to be able to work with them
            index = kwargs.get("index")
            obj = kwargs.get("instance")
            print(f"You picked\nIndex: {index}\nOption: {obj})

main_menu = MainMenu()

# Callbacks can also be defined after a menu instance has been initialized passing the instance as the first arg of the callback decorator

@callback(main_menu, index=1) #: index = 1 will match the second options
def option_2(**kwargs):
    #: **kwargs is mandatory as index and instance will be passed in order to be able to work with them
    index = kwargs.get("index")
    obj = kwargs.get("instance")
    print(f"You picked\nIndex: {index}\nOption: {obj})

main_menu.start()
```

- ### PynusMultiselect
This class is a subclass of ``PynusBase`` which allows to work with multi selection menus.

With this class user can pick multiple choices which will be returned by the ``PynusMultiselect.start()`` method.

The decorator ``@callback`` can be used with this class as well.
Leaving ``ìndex = None`` and ``obj = None`` in the ``@callback`` decorator will result in the
declared function to be called on every instance selected by the user.

#### How to use it

```python

from pynus import PynusMultiselect

class MultiselectMenu(PynusMultiselect):
    def __init__(self):
        super().__init__(
            title = "Multi selection menu, print out all choices",
            options = ["This", "is", "a", "multi", "selection", "menu"]
        )

        @callback(self)
        def print_out(**kwargs):
            instance = kwargs.get("instance")
            print(instance)

ms_menu = MultiselectMenu()

selections = ms_menu.start()

#: selections variable contains a list of all selected options
```

- ### Stack
The Stack class is no other than a modified list to which push the menus.
The menus will then be retreived in the opposite order or pushing to go back in the menu history.
To append the new menu to the Stack, just call the ``Stack().push()`` method.

The ``Stack().mainloop()`` method allows the execution of the menus.

#### How to use it

```python

from __future__ import annotations
from pynus import PynusBase, stack, callback


class Menu1(PynusBase):
    def __init__(self):
        super().__init__(title="Menu 1, select next menu", options=["To menu 2"])

        self.init_callbacks()

    def init_callbacks(self):
        @callback(self, index=0)
        def to_menu_2(**kwargs):
            stack.push(self)  #: Adds this menu to the stack chronology
            #: Return the next menu to be run in the next Stack().mainloop() iteration
            return Menu2()


class Menu2(PynusBase):
    def __init__(self):
        super().__init__(
            title="Menu 2, callback examples",
            options=[
                "Execute function and go back to previous menu",
                "Execute function and recall this menu (version 1)",
                "Execute function and recall this menu (version 2)",
                "Go to the next menu without adding the current one to the stack",
                "Go to the next menu adding the current one to the stack",
            ],
        )

        self.init_callbacks()

    def init_callbacks(self):
        @callback(self, index=0)
        def i0(**kwargs):
            index = kwargs.get("index")
            input(
                f"You choes option n° {index}\nPress ENTER to go to the previous menu..."
            )

            #: Returning None will call back the previous menu

        @callback(self, index=1)
        def i1(**kwargs):
            index = kwargs.get("index")
            input(
                f"You chose option n° {index}\nRecalling this menu, please press ENTER..."
            )

            #: Method 1 -> Adding this menu to the stack an return None
            stack.push(self)

        @callback(self, index=2)
        def i2(**kwargs):
            index = kwargs.get("index")
            input(
                f"You chose option n° {index}\nRecalling this menu, please press ENTER..."
            )

            #: Method 2 -> Returning self
            return self

        @callback(self, index=3)
        def i3(**kwargs):
            index = kwargs.get("index")
            input(
                f"You chose option n° {index}\nCalling the next menu without adding the current one to the stack, please press ENTER..."
            )

            return Menu3()

        @callback(self, index=4)
        def i4(**kwargs):
            index = kwargs.get("index")
            input(
                f"You chose option n° {index}\nCalling the next menu adding the current one to the stack, please press ENTER..."
            )

            #: Method 1 -> Adding this menu to the stack an return None
            stack.push(self)
            return Menu3()


class Menu3(PynusBase):
    def __init__(self):
        super().__init__(
            title="Choose Back to discover the effect of the previous choice",
            options=[],
        )


stack.push(Menu1())  #: Adding the first menu to the stack
stack.mainloop()  #: Running the mainloop

```



## License
MIT License

