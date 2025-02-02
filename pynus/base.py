from __future__ import annotations
from rainbow_pick import RainbowPicker
from .stack import Stack

stack = Stack()


class PynusBase(RainbowPicker):

    def __init__(self, title: str, options: list[object], instance: object = None):
        self.callbacks = {}
        options.append("Back")
        super().__init__(options, title)
        self.instance = instance

    def start(self):
        pick = super().start()

        if pick[0] == "Back":
            return None

        else:
            return self.callback(instance=pick[0], index=pick[1])

    @staticmethod
    def add_callback(menu: PynusBase, index=None, obj=None):
        def inner(callback_function: callable):
            if index is not None and not obj:
                menu.callbacks.update({index: callback_function})

            elif obj is not None and not index:
                menu.callbacks.update({obj: callback_function})

            elif not obj and not index:
                menu.callbacks.update({"all": callback_function})

            else:
                raise Exception("Only one between index and obj can be defined")

        return inner

    def callback(self, **kwargs):
        if "all" in self.callbacks.keys():
            return self.callbacks.get("all")(**kwargs)

        for key, func in self.callbacks.items():
            if kwargs.get("instance") == key or kwargs.get("index") == key:
                return func(**kwargs)


class PynusMultiselect(PynusBase):
    def __init__(self, title: str, options: list[object], instance: object = None):
        super().__init__(title, options, instance)
        self.options.pop()
        self.multiselect = True

    def start(self):
        picks = RainbowPicker.start(self)

        if not any(picks):
            return None

        common_function = self.callbacks.get("all")

        for pick in picks:
            if common_function:
                common_function(instance=pick[0], index=pick[1])
            for key, func in self.callbacks.items():
                if pick[0] == key or pick[1] == key:
                    func(instance=pick[0], index=pick[1])

        return picks


callback = PynusBase.add_callback
