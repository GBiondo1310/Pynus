from __future__ import annotations
from rainbow_pick import RainbowPicker


class PynusBase(RainbowPicker):
    """Base class for Pynus single choices menus"""

    matches: dict = {}

    def __init__(self, title: str, options: list[object], instance: object = None):
        """Initializes a PynusBas instance

        :param title: The title of the Pynus menu
        :type title: str
        :param options: The options to pick among
        :type options: list[object]
        :param instance: The instance to work on, defaults to None
        :type instance: object, optional"""

        options.append("Back")

        super().__init__(options, title)
        self.instance = instance

    def __call__(self, stack: Stack):
        """Runs the menu and calls the callback function on user's choice"""
        self.stack = stack
        pick = self.start()
        if pick[0] == "Back":
            return None  #: If None is returned, the stack will call ``self.back()`` in the mainloop
        else:
            return self.callback(instance=pick[0], index=pick[1])

    @classmethod
    def match_input(cls, index=None, obj=None):
        """Class method which adds a callback when a choice is match.

        :param index: The index chosen by the user
        :type index: int
        :param obj: The object chosen by the user
        :type obj: object

        :NOTE: Only one between index and obj can be defined, if both are defined, then
        this function will raise an error

        :USAGE:

        >>> class NewMenu(PynusBase):
        >>>     def __init__(self):
        >>>         super().__init__("New Menu", ["Option 1", Option 2", "Option 3"])
        >>>
        >>>     @PynusBase.match_input(index = 0)
        >>>     def option_1(self):
        >>>         print("You chose option 1")
        >>>
        >>>     @PynusBase.match_input(obj = "Option 2")
        >>>     def option_2(self):
        >>>         print("You chose option w")
        """

        def inner(callback_function: callable):
            if index is not None and not obj:
                cls.matches.update({index: callback_function})
            elif obj is not None and not index:
                cls.matches.update({obj: callback_function})
            else:
                raise Exception("Only one between index and obj can be defined")

        return inner

    def callback(self, **kwargs):
        for key, func in self.matches.items():
            if kwargs.get("instance") == key or kwargs.get("index") == key:
                return func(self)


class PynusMultiselect(RainbowPicker):
    """Base class for multiple selection menus"""

    matches: dict = {}

    def __init__(self, title: str, options: list[object], instance: object = None):
        """Initialize a PynusMultiselect instance

        :param title: The title of the Pynus mmenu
        :type title: str
        :param options: The options to pick among
        :type options: list[object]
        :param instance: The instance to work on if needed, defaults to None
        :type instance: object, optional"""

        super().__init__(options, title, multiselect=True)
        self.instance = instance

    def __call__(self):
        """Runs the menu"""
        return self.start()

    @classmethod
    def match_input(cls, instance: object = None):
        """Class method which adds a callback if the instance is present among user's picked choices
        if None is passed, then the method applies to all instance indistinctively

        :param instance: The instance chosen by the user, defaults to None
        :type isntance: object, optional"""

        def inner(callback_function: callable):
            cls.matches.update(
                {"all" if instance is None else instance: callback_function}
            )

        return inner

    def callback(self, instance: object):
        if "all" in self.matches.keys():
            return self.matches.get("all")(self)

        else:
            return self.matches.get(instance)(self)


class Stack(list):
    """Stack to store menus"""

    cur_menu = None

    def __init__(self):
        """Initializes the Stack"""

        super().__init__()
        self.cur_menu = None

    def __add__(self, menu: PynusBase):
        """Adds a new menu to the stack simply using the ``+`` operator

        :param menu: The new menu to add to the stack
        :type menu: PynusBased inheriting classes"""

        self.append(menu)

    def back(self):
        """Retreives the previous menu if any, else quits the application"""
        try:
            self.cur_menu = self.pop()
        except IndexError:
            quit()

    def main_loop(self):
        """The mainloop of the Stack"""
        while True:
            if not self.cur_menu:
                self.back()  #: If no menu is returned by the last one, the previous will be retreived

            self.cur_menu = self.cur_menu(self)
