class Stack(list):
    def __init__(self):
        super().__init__()

    def pop(self, index=-1):
        try:
            return super().pop(index)
        except IndexError:
            return None

    def push(self, object):
        object.index = 0
        return super().append(object)

    def mainloop(self):
        menu = self.pop()
        menu.index = 0
        while True:
            if not menu:
                menu = self.pop()
            if not menu:
                break

            menu = menu.start()
