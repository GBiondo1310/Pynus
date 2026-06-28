from pynus import PynusBase, Stack, callback


class LoggedMenu(PynusBase):
    def __init__(self):
        super().__init__("Menu", ["A", "B"])
        self.init_callbacks()

    def init_callbacks(self):
        @callback(self)  # Runs for every selection
        def log(**kwargs):
            print(f"[LOG] Option {kwargs['index']} selected")

        @callback(self, index=0)  # Runs after log()
        def option_a(**kwargs):
            print("Handling A")
            return self

        @callback(self, index=1)
        def option_b(**kwargs):
            print("Handling B")


stack = Stack()
stack.push(LoggedMenu())
stack.mainloop()
