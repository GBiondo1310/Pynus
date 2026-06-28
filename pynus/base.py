from __future__ import annotations
from rainbow_pick import RainbowPicker
from .stack import Stack

stack = Stack()


class PynusBase(RainbowPicker):

    def __init__(self, title: str, options: list[object], *, include_back: bool = True, **kwargs):
        self.callbacks = {}
        opt_list = list(options)
        if include_back:
            opt_list.append("Back")
        super().__init__(opt_list, title, **kwargs)

    def start(self):
        pick = super().start()

        if pick[0] == "Back":
            return None

        else:
            return self.callback(instance=pick[0], index=pick[1])

    @staticmethod
    def add_callback(menu: PynusBase, index=None, obj=None):
        def inner(callback_function: callable):
            if index is not None and obj is None:
                menu.callbacks.update({index: callback_function})

            elif obj is not None and index is None:
                menu.callbacks.update({obj: callback_function})

            elif index is None and obj is None:
                menu.callbacks.update({"all": callback_function})

            else:
                raise Exception("Only one between index and obj can be defined")

        return inner

    def callback(self, **kwargs):
        all_result = None
        if "all" in self.callbacks:
            all_result = self.callbacks["all"](**kwargs)

        for key, func in self.callbacks.items():
            if key == "all":
                continue
            if kwargs.get("instance") == key or kwargs.get("index") == key:
                return func(**kwargs)

        return all_result


class PynusMultiselect(PynusBase):
    def __init__(self, title: str, options: list[object], **kwargs):
        super().__init__(title, options, include_back=False, multiselect=True, **kwargs)

    def start(self):
        picks = RainbowPicker.start(self)

        if not any(picks):
            return None

        for pick in picks:
            self.callback(instance=pick[0], index=pick[1])

        return picks


callback = PynusBase.add_callback
