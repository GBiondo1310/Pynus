from .base import PynusBase, callback


class PynusYN(PynusBase):
    """Simple yet handy Yes / No menu"""

    def __init__(self, title: str):
        """Initializes the menu"""
        super().__init__(title, ["Yes", "No"])
        self.init_callbacks()

    def init_callbacks(self):
        @callback(self, index=0)
        def yes(**kwargs):
            return True

        @callback(self, index=1)
        def no(**kwargs):
            return False
