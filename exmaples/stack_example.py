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
                f"You chose option n° {index}\nPress ENTER to go to the previous menu..."
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
