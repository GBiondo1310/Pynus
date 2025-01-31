from pynus.base import PynusBase, Stack


class MenuTest1(PynusBase):
    def __init__(self, iterations):

        self.iterations = iterations

        self.options = [f"You've done {self.iterations} iterations, add 1"]

        super().__init__("Menu test 1", self.options, instance="asdrubale")

    @PynusBase.match_input(index=0)
    def add1(self):
        self.stack + self
        return MenuTest1(self.iterations + 1)


stack = Stack()

stack + MenuTest1(0)

stack.main_loop()
