from pynus import PynusBase, PynusMultiselect, stack, callback
from math import sqrt


class MainMenu(PynusBase):
    def __init__(self):
        super().__init__(
            "Basic operations menu",
            ["Single choice showcase", "Multiple choice showcase"],
        )
        self.init_callbacks()

    def init_callbacks(self):
        @callback(self, index=0)
        def to_single_choice_menu(**kwargs):
            stack.push(self)
            return SingleChoiceMenu()

        @callback(self, index=1)
        def to_multi_choice_menu(**kwargs):
            stack.push(self)
            choices = MultiChoicesMenu().start()
            #: You can do further operations with choices here


class SingleChoiceMenu(PynusBase):
    def __init__(self):
        super().__init__(
            "Single choice menu showcase, Pick a number to execute square root",
            ["121", "144", str(18**2)],
        )
        self.init_callbacks()

    def init_callbacks(self):
        @callback(self)
        def execute_square_root(**kwargs):
            num = int(kwargs.get("instance"))
            input(f"Square root of {num} is {sqrt(num)}\nPress ENTER to continue...")
            return self


class MultiChoicesMenu(PynusMultiselect):
    def __init__(self):
        super().__init__(
            "Multi choice menu showcase, pick numbers to execute powers",
            ["11", "12", "18"],
        )

        self.init_callbacks()

    def init_callbacks(self):
        @callback(self)
        def execute_power(**kwargs):
            num = int(kwargs.get("instance"))
            input(f"Second power of {num} is {num**2}\nPress ENTER to continue...")


stack.append(MainMenu())
stack.mainloop()
