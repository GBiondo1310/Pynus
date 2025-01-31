from .base import PynusBase, Stack


class PynusYN(PynusBase):
    """Simple yet handy Yes / No menu"""

    def __init__(self, title: str):
        """Initializes the menu"""

        super().__init__(title, ["Yes", "No"])

    match = PynusBase.match_input

    @match(index=0)
    def yes(self):
        return True

    @match(index=1)
    def no(self):
        return False
